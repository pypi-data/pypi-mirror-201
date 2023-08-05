# STIG ID:	RHEL-07-010130
# Rule ID:	SV-86529r5_rule
# Vuln ID:	V-71905
# SRG ID:	SRG-OS-000070-GPOS-00038
# Finding Level:	medium
#
# Rule Summary:
#	When passwords are changed or new passwords are established,
#	the new password must contain at least one lower-case
#	character.
#
# CCI-000193
#    NIST SP 800-53 :: IA-5 (1) (a)
#    NIST SP 800-53A :: IA-5 (1).1 (v)
#    NIST SP 800-53 Revision 4 :: IA-5 (1) (a)
#
#################################################################
{%- set stig_id = 'RHEL-07-010130' %}
{%- set helperLoc = 'ash-linux/el7/STIGbyID/cat2/files' %}
{%- set skipIt = salt.pillar.get('ash-linux:lookup:skip-stigs', []) %}
{%- set cfgFile = '/etc/security/pwquality.conf' %}
{%- set parmName = 'lcredit' %}
{%- set parmValu = '-1' %}
{%- set parmDesc = 'lowercase' %}

script_{{ stig_id }}-describe:
  cmd.script:
    - source: salt://{{ helperLoc }}/{{ stig_id }}.sh
    - cwd: /root

{%- if stig_id in skipIt %}
notify_{{ stig_id }}-skipSet:
  cmd.run:
    - name: 'printf "\nchanged=no comment=''Handler for {{ stig_id }} has been selected for skip.''\n"'
    - stateful: True
    - cwd: /root
{%- else %}
  {%- if salt.file.search(cfgFile, '^' + parmName) %}
file_{{ stig_id }}-{{ cfgFile }}:
  file.replace:
    - name: '{{ cfgFile }}'
    - pattern: '^{{ parmName }}.*$'
    - repl: '{{ parmName }} = {{ parmValu }}'
  {%- else %}
file_{{ stig_id }}-{{ cfgFile }}:
  file.append:
    - name: '{{ cfgFile }}'
    - text: |-
        # Inserted per STIG-ID {{ stig_id }}:
        # * Require new passwords to have at least one {{ parmDesc }} character
        {{ parmName }} = {{ parmValu }}
  {%- endif %}
{%- endif %}
