---
{% set instance_id = salt.pillar.get('instance_id') %}
{% set project = salt.pillar.get('gce_project') %}

"Restart start that server":
  salt.function:
    - tgt: 'dev-master*'
    - name: vcloud.start
    - kwarg:
        instance: {{ instance_id }}
        project: {{ project }}

