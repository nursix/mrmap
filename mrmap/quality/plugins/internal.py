"""
Author: Jan Suleiman
Organization: terrestris GmbH & Co. KG
Contact: suleiman@terrestris.de
Created on: 02.11.20

"""
import json
from datetime import datetime

from django.utils import timezone

from quality.enums import RulePropertyEnum
from quality.models import RuleSet, Rule, \
    ConformityCheckConfiguration, ConformityCheckConfigurationInternal, \
    ConformityCheckRun
from quality.settings import quality_logger
from service.models import Metadata
from structure.celery_helper import get_task_id, runs_as_async_task
from structure.models import PendingTask


class QualityInternal:

    def __init__(self, metadata: Metadata,
                 base_config: ConformityCheckConfiguration):
        self.metadata = metadata
        self.config = ConformityCheckConfigurationInternal.objects.get(
            pk=base_config.pk)

        count = self.config.mandatory_rule_sets.all().count() + \
                self.config.optional_rule_sets.all().count()

        try:
            self.step_size = 80 / count
        except ZeroDivisionError:
            self.step_size = 80

    def run(self) -> ConformityCheckRun:
        """ Runs the internal check for a given metadata object.

        Runs the mandatory and optional RuleSets of an internal check
        and updates the associated ConformityCheckRun accordingly.

        Returns:
            The ConformityCheckRun instance

        """
        run = ConformityCheckRun.objects.create(
            metadata=self.metadata, conformity_check_configuration=self.config)

        config = run.conformity_check_configuration

        results = {
            "success": True,
            "rule_sets": []
        }

        for rule_set in config.mandatory_rule_sets.all():
            mandatory_result = self.check_ruleset(rule_set)
            mandatory_result["name"] = str(rule_set)
            mandatory_result["id"] = rule_set.id
            mandatory_result["mandatory"] = True
            if not mandatory_result["success"]:
                results["success"] = False
            results["rule_sets"].append(mandatory_result)

            if runs_as_async_task():
                self.update_progress()

        for rule_set in config.optional_rule_sets.all():
            optional_result = self.check_ruleset(rule_set)
            optional_result["name"] = str(rule_set)
            optional_result["id"] = rule_set.id
            optional_result["mandatory"] = False
            results["rule_sets"].append(optional_result)

            if runs_as_async_task():
                self.update_progress()

        time_stop = timezone.now()
        results["time_start"] = str(run.time_start)
        results["time_stop"] = str(time_stop)

        run.passed = results["success"]
        run.time_stop = time_stop
        run.result = json.dumps(results)
        run.save()
        return run

    def check_ruleset(self, ruleset: RuleSet):
        """ Evaluates all rules of a ruleset for the given metadata object.

        Evaluates for each rule in a ruleset, if it evaluates to true or false.
        A ruleset will be flagged as successful, if all rules evaluated to true.

        Args:
            ruleset (RuleSet): The RuleSet to evaluate.
        Returns:
            {"success": bool, "rules": dict[]}
        """
        result = {
            "success": True,
            "rules": []
        }

        for rule in ruleset.rules.all():
            rule_result = self.check_rule(rule)

            rule_result.update(rule.as_dict())

            result["rules"].append(rule_result)
            if not rule_result["success"]:
                result["success"] = False
        return result

    def check_rule(self, rule: Rule):
        """ Evaluates a single rule for the given metadata object.

        Args:
            rule (Rule): The rule to evaluate.
        Returns:
            {"success": bool, "condition": str}: The result of the check.
        """
        prop = rule.property
        operator = rule.operator
        field = rule.field_name
        threshold = rule.threshold
        real_value = None

        if prop == RulePropertyEnum.LEN.value:
            attribute = self.metadata.__getattribute__(field)
            real_value = len(attribute)

        elif prop == RulePropertyEnum.COUNT.value:
            manager = self.metadata.__getattribute__(field)
            elements = manager.all()
            real_value = elements.count()

        condition = str(real_value) + operator + str(threshold)

        return {
            "success": eval(condition, {'__builtins__': None}),
            "condition": condition
        }

    def update_progress(self):
        """Update the progress of the pending task."""
        task_id = get_task_id()
        try:
            pending_task = PendingTask.objects.get(task_id=task_id)
            progress = pending_task.progress + self.step_size
            # we should only set the progress to max 90
            # as the calling method might also update the progress
            pending_task.progress = progress if progress <= 90 else 90
            pending_task.save()
        except PendingTask.DoesNotExist:
            quality_logger.error(
                f'Could not update pending task. Task with id {task_id} does '
                f'not '
                f'exist.')