Ferm
=================

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

- You MUST set `ferm.enable` variable. It's mandatory.
- Variable `ferm.fermd` is optional and contain list of installed configs from {{ playbook_dir }}.
- Variable `ferm.only_includes` is optional and  responsible for disabling default rules in template. Set it to `true` if you want to only use rules from ferm.d.

```

ferm:
  enable: true
  only_includes: false
  fermd:
    - iface_br1_allow_all
    - nginx_rules

```

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
