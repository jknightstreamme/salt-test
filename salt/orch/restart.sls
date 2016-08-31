---
{% set instance_id = salt.pillar.get('instance_id', 'test') %}
{% set project = salt.pillar.get('gce_project', 'test-project') %}

vcloud.start:
  salt.function:
    - tgt: 'dev-master*'
    - kwarg:
        instance: {{ instance_id }}
        project: {{ project }}

