+++
title = "Azure Resource Naming"
date = 2021-08-02
updated = 2025-10-12
+++

Naming Azure resources can be difficult. You want to include relevant information into the name, but also not make it too long too remember. You want to keep your names consistent, but some things are different per project. In addition, some resources have restrictions on the characters allowed or the length.

Here's my naming standard:

All non-name-limited Azure resources attempt to use the following standard:

```
[project]-[part...]-[resource-type]-[env]-[client]
```

- `[project]` : the overarching name of the project -  Example: `mywebapp` for some webapp
- `[part...]` : project-specific dash-delimited words. For example, instance number, or location code, or subpart. - Example: `admin`, `admin-wus2-01`. If the project is simple enough to not have parts, just use `01`
- `[resource-type]` : short resource type abbreviation - Example: `kv` for Key Vault. There is in incomplete list of abbreviations [here](https://docs.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations)
- `[env]` : One of `dev`, `test`, `prod`
- `[client]`: Owner of the project - Example: `bbk` (short for my org, bbkane.com) . Useful to ensure globally unique names or to stand up instances of the same project for different clients

Some resources have name limitations. For example, storage account names must be globally unique, can only use alpha-numeric characters, and are limited to 24 characters in length. These resource types should “do their best” to follow the standard.

Example: A web app called `mywebapp`

- `mywebapp-admin-rg-dev-bbk` - resource group
- `mywebapp-01-sp-dev-bbk` - service prinicipal
- `mwauserinfosadevbbk`  - storage account

Azure AD names (users, groups, …) are shared among subscriptions in a tenant and should use the following naming convention: [project]-[part]

Also see:

- [Define your naming convention - Cloud Adoption Framework | Microsoft Learn](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming)
- [Navnkonvensjoner i Azure](https://www.ironstoneit.com/no/artikler/naming-conventions-for-azure)
- [Adventures with Azure: Regions – Matt Ruma](https://mattruma.com/adventures-with-azure-regions/)
