import { Alert, Button, Form, notification, Select, Space } from 'antd';
import { useForm } from 'antd/lib/form/Form';
import { default as React, ReactElement, useEffect, useState } from 'react';
import { useNavigate } from 'react-router';
import { useParams } from 'react-router-dom';
import WmsAllowedOperationRepo, { WmsAllowedOperationCreate } from '../../../Repos/WmsAllowedOperationRepo';
import WmsOperationRepo from '../../../Repos/WmsOperationRepo';
import { InputField } from '../../Shared/FormFields/InputField/InputField';

const { Option } = Select;

const wmsOpRepo = new WmsOperationRepo();

interface RuleFormProps {
    wmsId: string,
    selectedLayerIds: string[],
    setSelectedLayerIds: (ids: string[]) => void    
}

export const RuleForm = ({
  wmsId,
  selectedLayerIds,
  setSelectedLayerIds
}: RuleFormProps): ReactElement => {

  const ruleRepo = new WmsAllowedOperationRepo(wmsId);

  const navigate = useNavigate();
  const { ruleId } = useParams();
  const [form] = useForm();
  const [availableOps, setAvailableOps] = useState<typeof Option[]>([]);
  const [validationErrors, setValidationErrors] = useState<string[]>([]);  

  useEffect(() => {
    let isMounted = true;
    async function initAvailableWmsOps () {
      const jsonApiResponse = await wmsOpRepo.findAll() as any;
      const wmsOps = jsonApiResponse.data.data.map((wmsOp: any) => 
        (<Option value={wmsOp.id} key={wmsOp.id}>{wmsOp.id}</Option>)
      );
      isMounted && setAvailableOps(wmsOps);
    }
    async function fetchRuleAndInitForm (id: string) {
      const jsonApiResponse = await ruleRepo.get(id) as any;
      if (isMounted) {
        form.setFieldsValue({
          description: jsonApiResponse.data.data.attributes.description,
          operations: jsonApiResponse.data.data.relationships.operations.data.map((operation: any) => 
            operation.id
          )
        });
        const securedLayerIds = jsonApiResponse.data.data.relationships.secured_layers.data.map((layer: any) => 
          layer.id
        );
        setSelectedLayerIds(securedLayerIds);
      }
    }
    isMounted && initAvailableWmsOps();
    isMounted && ruleId && fetchRuleAndInitForm(ruleId);
    return (() => { isMounted = false; });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  },[ruleId]);

  const onFinish = (values: any) => {
    if (selectedLayerIds.length === 0) {
      setValidationErrors(['At least one layer needs to be selected.']);
      return;
    }
    async function create () {
      const createObj: WmsAllowedOperationCreate = {
        description: values.description,
        securedLayerIds: selectedLayerIds,
        allowedOperationIds: values.operations,
        allowedGroupIds: [] // TODO
      };      
      const res = await ruleRepo.create(createObj);
      if (res.status === 201) {
        notification.info({
          message: 'WMS security rule created',
          description: 'Your WMS security rule has been created'
        });
        navigate(`/registry/services/wms/${wmsId}/security`);
      }
    }
    async function update (ruleId: string) {
      const attributes = {
        description: values.description
      };
      const relationships = {
        'secured_layers': {
          'data': selectedLayerIds.map((id) => {
            return {
              type: 'Layer',
              id: id
            };
          })
        },
        'operations': {
          'data': values.operations.map((id: any) => {
            return {
              type: 'WebMapServiceOperation',
              id: id
            };
          })
        }
      };
      const res = await ruleRepo.partialUpdate(ruleId, 'AllowedWebMapServiceOperation', attributes, relationships);
      if (res.status === 200) {
        notification.info({
          message: 'WMS security rule updated',
          description: 'Your WMS security rule has been updated'
        });
        navigate(`/registry/services/wms/${wmsId}/security`);
      }
    }    
    ruleId ? update(ruleId) : create();
  };

  return (
    <>
      <Form
        form={form}
        layout='vertical'
        onFinish={onFinish}
      >
        <InputField
          label='Description'
          name='description'
          placeholder='Short description of the security rule'
          validation={{
            rules: [{ required: true, message: 'Please input a description!' }],
            hasFeedback: false
          }}
        />
        <Form.Item 
          label='Operations'
          name='operations'
          required={true}
          rules={[{ required: true, message: 'At least one operation must be selected!' }]}
        >
          <Select
            mode='multiple'
            allowClear
            placeholder='Allowed WMS operations'
          >
            {availableOps}
          </Select>
        </Form.Item>
        {
          validationErrors.map((error, i) => (
            <Form.Item key={i}>
              <Alert
                description={error}
                type='error'
              />
            </Form.Item>
          ))
        }
        <Form.Item>
          <Space>
            <Button
              type='primary'
              htmlType='submit'
            >
              Speichern
            </Button>
            <Button
              htmlType='button'
              onClick={ () => navigate(`/registry/services/wms/${wmsId}/security`)}
            >
              Abbrechen
            </Button>
          </Space>
        </Form.Item>
      </Form>
    </>
  );
};
