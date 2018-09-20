var card = new function() {
	   
	this.existBalanceRefund = function(cardNo) {
		
		var isExist = true;
		$.ajax({
			url: "/api/card/"+cardNo+"/balance-refund/exist", /* cardApi.existBalanceRefund() */
			type: 'GET',
			dataType : "json",
			contentType  : "application/json",
			async : false,
			success: function(result){
				if(result.status === 200) {
					if (result.data) {
						isExist = true;
					}
					else {
						isExist = false;
					}
				}
				else if (result.status == 500) {
					kpcUtil.customAlert(result.message);
				}
             },
             error : function(e){
            	 kpcUtil.errorHandling(e);
             }
         })
         return isExist;
    },
	
    this.getBalanceRefundStatus = function(status) {
		var statusName = "";

		if(status === "PROC-0010") {
			statusName = "환불승인";
		}
		else if (status === "PROC-0050") {
			statusName = "<font color='red'>환불불가</font>";
		}
		else if (status === "PROC-0040") {
			statusName = "환불완료";
		}
		
		return statusName;
    }
    
}


