param resourceGroupName string = 'cognitive-rg'
param accountName string = getenv('ACCOUNT_NAME')
param location string = resourceGroup().location
param sku string = getenv('SKU')

resource cognitiveAccount 'Microsoft.CognitiveServices/accounts@2021-10-01' = {
  name: accountName
  location: location
  kind: 'ComputerVision'
  sku: {
    name: sku
  }
  properties: {}
}

output endpoint string = reference(cognitiveAccount.id, cognitiveAccount.apiVersion).properties.endpoint