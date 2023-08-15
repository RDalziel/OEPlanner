targetScope = 'resourceGroup'

param location string
param appName string

var uiAppServiceName = '${appName}ui'
var workerAppServiceName = '${appName}worker'
var apiAppServiceName = '${appName}api'
var appInsightsName = '${appName}insights'  
var logAnalyticsName = '${appName}analytics'
var appServicePlanName = '${appName}appplan'
var serviceBusName = '${appName}bus'
var identityName = '${appName}identity'


resource managedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2021-09-30-preview' = {
  name: identityName
  location: location
}

resource serviceBusRoleAssignment 'Microsoft.Authorization/roleAssignments@2020-10-01-preview' = {
  name: guid(managedIdentity.id, serviceBus.id)
  properties: {
    principalId: managedIdentity.properties.principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '090c5cfd-751d-490a-894a-3ce6f1109419')
  }
  scope: serviceBus
}

resource appServicePlan 'Microsoft.Web/serverfarms@2021-03-01' = {
  name: appServicePlanName
  location: location
  kind: 'linux'
  properties: {
    reserved: true
  }
  sku: {
    name: 'B1'
    capacity: 1
  }
}

resource serviceBus 'Microsoft.ServiceBus/namespaces@2022-01-01-preview' = {
  name: serviceBusName
  location: location
  sku: {
    name: 'Standard'
  }
  properties: {
    zoneRedundant: false
  }
}



resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web' 
  properties: {
     Application_Type: 'web'
     WorkspaceResourceId: logAnalytics.id
  }
}

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2021-12-01-preview' = {
  name: logAnalyticsName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    workspaceCapping: {
      dailyQuotaGb: 1
    }
  }
}

resource uiAppService 'Microsoft.Web/sites@2021-03-01' = {
  name: uiAppServiceName
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${managedIdentity.id}' : {}
    }
  }
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      appSettings: [
        {
          name: 'AZURE_CLIENT_ID'
          value: managedIdentity.properties.clientId
        }
        {
          name: 'AZURE_TENANT_ID'
          value: subscription().tenantId
        } 
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsights.properties.ConnectionString
        }
      ] 
    }
  }
}


var serviceBusEndpoint = '${serviceBus.id}/AuthorizationRules/RootManageSharedAccessKey' 
var amqpUrl = 'azureservicebus://RootManageSharedAccessKey:${listKeys(serviceBusEndpoint, serviceBus.apiVersion).primaryKey}@${serviceBus.name}.servicebus.windows.net'

resource workerAppService 'Microsoft.Web/sites@2021-03-01' = {
  name: workerAppServiceName
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${managedIdentity.id}' : {}
    }
  }
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.10'
      appSettings: [
        {
          name: 'AZURE_CLIENT_ID'
          value: managedIdentity.properties.clientId
        }
        {
          name: 'AZURE_TENANT_ID'
          value: subscription().tenantId
        } 
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsights.properties.ConnectionString
        }
        {
          name: 'CELERY_BROKER_URL'
          value: amqpUrl
        }
      ] 
    }
  }
}



resource apiAppService 'Microsoft.Web/sites@2021-03-01' = {
  name: apiAppServiceName
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${managedIdentity.id}' : {}
    }
  }
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.10'
      appSettings: [
        {
          name: 'AZURE_CLIENT_ID'
          value: managedIdentity.properties.clientId
        }
        {
          name: 'AZURE_TENANT_ID'
          value: subscription().tenantId
        } 
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsights.properties.ConnectionString
        }
        {
          name: 'CELERY_BROKER_URL'
          value: amqpUrl
        }
      ] 
    }
  }
}

