# JavaScript Notes:

# 1. Override an existing Component:

1. create a file in `static/src/js/file_name.js`.
2. add the file to the `__manifest__.py` in , like the following:

```
'assets': {
        'web.assets_backend': [
            '/module_name/static/src/js/file_name.js',
        ]
    },
```

3. in the `file_name.js` add at the top `/** @odoo-module **/`.

### here an example of the code:

```
/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { AnalyticDistribution } from "@analytic/components/analytic_distribution/analytic_distribution";

patch(
	AnalyticDistribution.prototype,
	"seed_accounting_customization.AnalyticDistribution",
	{
		/**
		 * @override
		 */
		// Getters;
		get tags() {
			return this.listReady.map((dist_tag) => ({
				id: dist_tag.id,
				text: ` ${this.getAnalyticName(dist_tag)}${
					dist_tag.percentage > 99.99 && dist_tag.percentage < 100.01
						? ""
						: " " + this.formatPercentage(dist_tag.percentage)
				}`,
				colorIndex: dist_tag.color,
				group_id: dist_tag.group_id,
				onClick: (ev) => this.tagClicked(ev, dist_tag.id),
				onDelete: this.editingRecord
					? () => this.deleteTag(dist_tag.id)
					: undefined,
			}));
		},

	}
);

```
### Here is the explanation:
```
/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { AnalyticDistribution } from "@analytic/components/analytic_distribution/analytic_distribution";

patch(
	ComponentName.prototype,
	"your_module_name.ComponentName",
	{
		# action

	}
);
```
- `patch` is used to override an existing component.
### `Note`: check `seed_accounting_customization` for the actual code.
