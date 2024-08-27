odoo.define('masterspbu.month_year_widget', function (require) {
    "use strict";

    var fieldRegistry = require('web.field_registry');
    var AbstractField = require('web.AbstractField');

    var MonthYearWidget = AbstractField.extend({
        template: 'MonthYearWidget',
        supportedFieldTypes: ['char'],

        _render: function () {
            this.$el.text(this.value);
        },
    });

    fieldRegistry.add('month_year_widget', MonthYearWidget);

    return MonthYearWidget;
});