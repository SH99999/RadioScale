# VOLUMIO 4 PLUGIN CONFIG CONTRACT V1

Status: authoritative integration standard.

## Purpose

This contract defines the minimum configuration structure requirements for Volumio 4 plugin deliverables in this project.

## Leading rule

A plugin is not considered integration-ready if Volumio shows `configuration not available` for that plugin unless the plugin is explicitly documented as having no user-facing configuration.

## Expected plugin configuration artifacts

For Volumio plugins in this project, the canonical expectation is:
- `config.json`
- `UIConfig.json`
- `requiredConf.json` when the plugin depends on declared runtime prerequisites

## Plugin categories

### User interface plugins
Expected to expose a valid UI configuration surface when configuration is intended.
Examples in project context:
- tuner overlay plugin
- bridge plugin
- fun-line overlay plugin

### Music service plugins
Expected to expose a valid plugin configuration contract when configuration is intended.
Examples in project context:
- tuner source plugin

## Quality gate

A plugin fails the configuration contract if:
- `config.json` is missing,
- `UIConfig.json` is missing where a configurable UI is expected,
- configuration loads with `configuration not available` due to malformed or missing config structure,
- configuration schema is inconsistent with the runtime plugin id or plugin category.

## Current practical reference

Bridge is the current best reference model for Volumio 4 configuration behavior in this project.
That does not automatically make Bridge the global schema owner, but it is the current reference when other components are normalized.

## Required normalization outcome

All future plugin-capable components must document:
- plugin id
- plugin category
- config file set
- expected configuration visibility in Volumio
- validation method for the configuration page
