---
{% set instance_id = pillar.get('instance_id', 'test') %}
{% set project = pillar.get('gce_project', 'test-project') %}

vcloud.start:
  salt.function:
    - tgt: 'dev-master*'
    - kwarg:
        instance: {{ instance_id }}
        project: {{ project }}

