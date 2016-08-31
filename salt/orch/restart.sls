---

{% set instance_id = salt.pillar.get('instance_id') %}
{% set project = salt.pillar.get('gce_project') %}

vcloud.start:
  salt.function:
    - tgt: 'dev-master*'
    - kwarg:
        instance: {{ instance_id }}
        project: {{ project }}

