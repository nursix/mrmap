Feature: MapContext Rendering Layer
    As a User, 
    I want to configure the rendering behaviour of a layer, 
    So that the rendering configuration is part of the mapcontext.

  Background: Open mapcontext add page
    Given I am logged in as "mrmap" with password "mrmap"
    And the base url is "https://localhost:8000"
    And I open the site "/registry/mapcontexts/add"
    When I set "mapctx" to the inputfield "//*[@id='id_title']"
    And I set "short example of a mapcontext" to the inputfield "//*[@id='id_abstract']"
    And I click on the button "//*[@id='j1_1']//*[contains(@title, 'Add Folder')]"
    And I click on the element "//*[@id='j1_1_anchor']"
    And I click on the element "//*[@id='j1_2_anchor']"
    And I set "node1" to the inputfield "//*[@id='id_layer-1-name']"

  # Scenario: Successful configure mapcontext layer tree without offerings
  #   And I submit the form "//body//form"
  #   Then I wait on element "//*[contains(text(), 'mapctx')]" for 1000ms

  Scenario: Check correct form logic for scale min max fields if scale min max is a int or float
    When I scroll to element "//*[@aria-labelledby='select2-id_layer-0-rendering_layer-container']"
    When I click on the element "//*[@aria-labelledby='select2-id_layer-0-rendering_layer-container']"
    When I click on the element "//input[@class='select2-search__field']"
    When I set "Gemeindestrassen 1" to the inputfield "//input[@class='select2-search__field']"
    When I pause for 500ms
    When I press "Enter"
    Then I expect that element "//*[@id='id_layer-0-layer_scale_min']" is enabled
    And I expect that element "//*[@id='id_layer-0-layer_scale_min']" is enabled

  # Scenario: Check correct form logic for scale min max fields if scale min max is not a int or float
  #   When I click on the element "//select[@id='id_layer-0-rendering_layer']"
  #   When I click on the element "//input[@class='select2-search__field']"
  #   When I set "Relative Feuchte" to the inputfield "//input[@class='select2-search__field']"
  #   When I pause for 500ms
  #   When I press "Enter"
  #   Then I expect that element "//*[@id='id_layer-0-layer_scale_min']" is not enabled
  #   And I expect that element "//*[@id='id_layer-0-layer_scale_min']" is not enabled

