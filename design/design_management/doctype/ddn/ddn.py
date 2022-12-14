# Copyright (c) 2022, Rehan Ansari and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DDN(Document):
	pass
	def before_save(self):
		if self.items:
			for i in self.items:
				actual_qty = frappe.db.get_value('Design Bin', {'warehouse': i.source_warehouse,'item_code':i.item_code},'actual_qty')
				if actual_qty:
					qty = 0
					for j in self.items:
						if i.item_code == j.item_code:
							qty = j.qty + qty
					if actual_qty < qty:
						#frappe.throw("Available Qty in "+i.source_department +" is "+ str(actual_qty))
						frappe.throw(("Quantity not available for "+frappe.bold(i.item_code)+" in warehouse "+frappe.bold(i.source_warehouse)
						+ "<br><br>"
						+("Available quantity is "+frappe.bold(actual_qty)+", you need "+frappe.bold(float(qty)))
						),
							title=("Insufficient Stock"),
						)
					# if actual_qty < i.qty:
					#     frappe.throw("Available Qty in "+i.source_department +" is "+ str(actual_qty))
				else:
					frappe.throw("Qty not available in "+i.source_warehouse)
				if i.source_warehouse == i.target_warehouse:
					frappe.throw("Source and Target Department cannot be same")
	def on_submit(self):
		if self.items:
			for i in self.items:
				tar_doc = frappe.db.get_all('Design Bin',filters={'item_code': i.item_code,'warehouse':i.target_warehouse},fields=['name','actual_qty'])
				bin_doc = frappe.db.get_all('Design Bin',filters={'item_code': i.item_code,'warehouse':i.source_warehouse},fields=['name','actual_qty'])
				if tar_doc:
					ledger_minus_entry = frappe.get_doc({
						"doctype":"Design Ledger Entry",
						"item_code":i.item_code,
						"warehouse":i.source_warehouse,
						"posting_date":frappe.utils.nowdate(),
						"posting_time":frappe.utils.nowtime(),
						"voucher_type":"DDN",
						"voucher_no":self.name,
						"qty_change":-i.qty,
						"qty_after_transaction":bin_doc[0].actual_qty - i.qty,
						"revision":i.item_code+"-"+i.revision,
						"revision_id":i.revision,
						"revision_no":i.revision
					}).insert(ignore_permissions=True,ignore_mandatory=True)
					ledger_minus_entry.save()
					ledger_plus_entry = frappe.get_doc({
						"doctype":"Design Ledger Entry",
						"item_code":i.item_code,
						"warehouse":i.target_warehouse,
						"posting_date":frappe.utils.nowdate(),
						"posting_time":frappe.utils.nowtime(),
						"voucher_type":"DDN",
						"voucher_no":self.name,
						"qty_change":i.qty,
						"qty_after_transaction":tar_doc[0].actual_qty + i.qty,
						"revision":i.item_code+"-"+i.revision,
						"revision_id":i.revision,
						"revision_no":i.revision
					}).insert(ignore_permissions=True,ignore_mandatory=True)
					ledger_plus_entry.save()
				else:
					bin_doc = frappe.db.get_all('Design Bin',filters={'item_code': i.item_code,'warehouse':i.source_warehouse},fields=['name','actual_qty'])
					ledger_minus_entry = frappe.get_doc({
						"doctype":"Design Ledger Entry",
						"item_code":i.item_code,
						"warehouse":i.source_warehouse,
						"posting_date":frappe.utils.nowdate(),
						"posting_time":frappe.utils.nowtime(),
						"voucher_type":"DDN",
						"voucher_no":self.name,
						"qty_change":-i.qty,
						"qty_after_transaction":bin_doc[0].actual_qty - i.qty,
						"revision":i.item_code+"-"+i.revision,
						"revision_id":i.revision,
						"revision_no":i.revision
					}).insert(ignore_permissions=True,ignore_mandatory=True)
					ledger_minus_entry.save()
					ledger_entry = frappe.get_doc({
						"doctype":"Design Ledger Entry",
						"item_code":i.item_code,
						"warehouse":i.target_warehouse,
						"posting_date":frappe.utils.nowdate(),
						"posting_time":frappe.utils.nowtime(),
						"voucher_type":"DDN",
						"voucher_no":self.name,
						"qty_change":i.qty,
						"qty_after_transaction":i.qty,
						"revision":i.item_code+"-"+i.revision,
						"revision_id":i.revision,
						"revision_no":i.revision
					}).insert(ignore_permissions=True,ignore_mandatory=True)
					ledger_entry.save()
	def on_cancel(self):
		for i in self.items:
			lst_doc = frappe.db.get_all('Design Ledger Entry',filters={'voucher_no': self.name,'is_cancelled': 0},fields=['name','item_code','warehouse','qty_change'])
			if lst_doc:
				for j in lst_doc:
					frappe.db.set_value('Design Ledger Entry', j.name, 'is_cancelled', 1)
					bin_update = frappe.db.get_all('Design Bin',filters={'warehouse': j.warehouse,'item_code': j.item_code},fields=['name'])
					actual_qty = frappe.db.get_value('Design Bin', bin_update[0].name, 'actual_qty')
					update_qty = actual_qty - j.qty_change
					frappe.db.set_value('Design Bin', bin_update[0].name, 'actual_qty', update_qty)
