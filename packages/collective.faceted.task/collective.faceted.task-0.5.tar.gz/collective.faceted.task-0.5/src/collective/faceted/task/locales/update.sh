#!/bin/bash

domains=("collective.faceted.task" "eea")
#i18ndude sync --pot $domain.pot */LC_MESSAGES/$domain.po

for lang in $(find . -mindepth 1 -maxdepth 1 -type d); do
        for domain in "${domains[@]}"; do
                if test -d $lang/LC_MESSAGES; then
                        i18ndude rebuild-pot --pot $domain.pot --create $domain ../
                        touch $lang/LC_MESSAGES/$domain.po
                        i18ndude sync --pot $domain.pot $lang/LC_MESSAGES/$domain.po
                fi
        done
done
