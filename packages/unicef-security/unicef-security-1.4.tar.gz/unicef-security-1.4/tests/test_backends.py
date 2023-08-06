from social_core.tests.backends.test_azuread_b2c import AzureADB2COAuth2Test


class UNICEFAzureADTenantOAuth2ExtTest(AzureADB2COAuth2Test):
    backend_path = "unicef_security.backends.UNICEFAzureADTenantOAuth2Ext"
