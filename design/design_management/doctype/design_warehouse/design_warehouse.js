// Copyright (c) 2022, Rehan Ansari and contributors
// For license information, please see license.txt

frappe.ui.form.on('Design Warehouse', {
	refresh: function(frm) {
		frm.refresh_field("status");
	}
});