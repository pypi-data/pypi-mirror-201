CREATE_OR_UPDATE_MONTE_CARLO_CONFIG_TEMPLATE = """
mutation createOrUpdateMonteCarloConfigTemplate($namespace: String!, $configTemplateJson: String!, 
    $dryRun: Boolean, $misconfiguredAsWarning: Boolean,  $resource: String) {
  createOrUpdateMonteCarloConfigTemplate(
    configTemplateJson: $configTemplateJson,
    namespace: $namespace,
    dryRun: $dryRun,
    misconfiguredAsWarning: $misconfiguredAsWarning,
    resource: $resource            
  ) {
    response {
      resourceModifications {
        type
        description
        resourceAsJson
      }
      changesApplied
      errorsAsJson
      warningsAsJson
    }
  }
}
"""

DELETE_MONTE_CARLO_CONFIG_TEMPLATE = """
mutation deleteMonteCarloConfigTemplate($namespace: String!, $dryRun: Boolean) {
  deleteMonteCarloConfigTemplate(
    namespace: $namespace,
    dryRun: $dryRun
  ) {
    response {
      changesApplied
      numDeleted
    }
  }
}
"""
