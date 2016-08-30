---
{% set tag = salt.pillar.get('instance_id') %}

"Restart start that server":
  salt.function:
    - tgt: 'dev-master*'
    - name: cloud.action
    - kwarg:
      - fun: start
      - instance:
        - {{ data['id'] }}
