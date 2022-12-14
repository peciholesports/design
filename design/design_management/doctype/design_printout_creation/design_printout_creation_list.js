frappe.listview_settings['Design Printout Creation'] = {
    hide_name_column: true,
    add_fields: ["status"],
     get_indicator:function(doc){
		if(doc.status == 'To Receive and Return') {
			return [__("To Receive and Return"), "blue", "status,=,Closed"];
		} 
        else if (doc.status === "Created") {
			return [__("Created"), "green", "status,=,Closed"];
		}
		else if (doc.status === "To Receive") {
			return [__("To Receive"), "green", "status,=,Closed"];
		}
        else if (doc.status === "Recevied") {
			return [__("Recevied"), "green", "status,=,Closed"];
		}
        else if (doc.status === "To Return") {
			return [__("To Return"), "orange", "status,=,Closed"];
		}
        else if (doc.status === "Returned") {
			return [__("Returned"), "green", "status,=,Closed"];
		}
        else if (doc.status === "To Return Receive") {
			return [__("To Return Receive"), "orange", "status,=,Closed"];
		}
        else if (doc.status === "Completed") {
			return [__("Completed"), "green", "status,=,Closed"];
		}
        //  else if (flt(doc.per_returned, 2) === 100) {
		// 	return [__("Return Issued"), "grey", "per_returned,=,100"];
		// } else if (flt(doc.grand_total) !== 0 && flt(doc.per_billed, 2) < 100) {
		// 	return [__("To Bill"), "orange", "per_billed,<,100"];
		// } else if (flt(doc.grand_total) === 0 || flt(doc.per_billed, 2) === 100) {
		// 	return [__("Completed"), "green", "per_billed,=,100"];
		// }
        // else if (doc.status === "Draft") {
        //     return [__("Draft"), "red"];
        // }
        // else if(doc.status === "Return Issued"){
        //   return [__("Return Issued"), "yellow"];
        // }
        // else if(doc.status === "Cancelled"){
        //   return [__("Cancelled"), "red"];
        // }
     }
};