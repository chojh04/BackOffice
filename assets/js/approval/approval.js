
/**
 * 재승인이 가능한지 확인
 * @param workType
 * @param refId
 * @returns
 */

var approval = new function() {

	this.existApprovalRequest = function(refId) {
		
		var isExist = true;
		$.ajax({
			url: "/api/approvals/request/"+refId+"/exist",
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

    this.existBillingByServiceId = function(serviceId) {
    	
    	var isExistBilling = true;
    	$.ajax({
    		url: "/api/approvals/request/billing/exist/"+serviceId,
    		type: 'GET',
    		dataType : "json",
    		contentType  : "application/json",
    		async : false,
    		success: function(result){
    			if(result.status === 200) {
    				if (result.data) {
    					alert("정산정보가 등록되어 있습니다.");
    				}
    				else {
    					isExistBilling = false;
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
    	return isExistBilling;
    },
	
	this.possibleReApproval = function(workType, refId) {
    	
    	var alertMessage = "";
    	if (workType === "AWRK-0001") {
    		alertMessage = "이미 삭제된  대표거래처 입니다.";
    	}
    	else if (workType === "AWRK-0002") {
    		alertMessage = "이미 삭제된 일반거래처 입니다.";
    	}
    	else if (workType === "AWRK-0003") {
    		alertMessage = "이미 삭제된 서비스 정보 입니다.";
    	}
    	else if (workType === "AWRK-0004") {
    		alertMessage = "이미 삭제된 정산 정보 입니다.";
    	}
    	else if (workType === "AWRK-0005") {
    		alertMessage = "이미 삭제된 쿠폰 상품 입니다.";
    	}
    	else if (workType === "AWRK-0006") {
    		alertMessage = "정산내역 조정";
    	}
    	else if (workType === "AWRK-0007") {
    		alertMessage = "경비";
    	}
    	else if (workType === "AWRK-0008") {
    		alertMessage = "이미 삭제된 정산 수수료 정보 입니다.";
    	}
    	else if (workType === "AWRK-0009") {
    		alertMessage = "이미 삭제된 KCON 상품 정보 입니다.";
    	}
    	else if (workType === "AWRK-0010") {
    		alertMessage = "이미 발행 취소된 KCON 쿠폰 정보입니다.";
    	}
    	else if (workType === "AWRK-0011") {
    		alertMessage = "잔액이 없는 카드 정보입니다.";
    	}
    	
		var isPossible = false;
		$.ajax({
			url: "/api/approvals/request/"+workType+"/"+refId+"/re-approval/possibility",
			type: 'GET',
			dataType : "json",
			contentType  : "application/json",
			async : false,
			success: function(result){
				if(result.status === 200) {
					if (result.data) {
						isPossible = true;
					}
					else {
						kpcUtil.customAlert(alertMessage);
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
		 
		 return isPossible;
	}
    
    
    /**
     * 알림 정보(notiInfo)에는 apprEmpId, message, approvalType이 있다.
     * 
     * var notiInfo = {
     * 		"receiverEmpId" : "받을 사용자 사번",
     * 		"message" : "보낼 메시지",
     * 		"approvalType" : "request(승인요청), answer(승인처리)"
     * }
     * 
     */
    this.notificationSmsService = function(notiInfo) {
    	
		$.ajax({
			url: "/api/approvals/notification",
			type: 'POST',
			data: JSON.stringify(notiInfo),
			dataType : "json",
			contentType  : "application/json",
			async : false,
			error : function(e){
				console.log(e)
			}
		 })
    }
    
	this.approvalAnswerSendSms = function(data, answerType) {
				
		var workTypeName = this.getApprovalWorkType(data.workType);
		var reqTypeName = this.getApprovalReqType(data.reqType);
		
		var message = "";		
		if (answerType === "approve") {
			message = "[R2 - "+workTypeName+" : "+reqTypeName+"] 승인완료 처리되었습니다. 승인 신청내역에서 확인해주세요.";
		}
		else if (answerType === "reject") {
			message = "[R2 - "+workTypeName+" : "+reqTypeName+"] 승인반려 처리되었습니다. 승인 신청내역에서 확인해주세요.";	
		}
		
		/* -------------------------------------  */
		var notiInfo = {
				"receiverEmpId" : data.reqEmpId,
				"message" : message,
				"approvalType" : "answer"
		}
		
		console.log(notiInfo);
		
		//문자 보내기
		this.notificationSmsService(notiInfo);
		/* -------------------------------------  */
	}

	
    this.getApprovalWorkType = function(workType) {
		var workTypeName = "";

		if(workType === "AWRK-0001") {
			workTypeName = "대표 거래처";
		}
		else if (workType === "AWRK-0002") {
			workTypeName = "일반 거래처";
		}
		else if (workType === "AWRK-0003") {
			workTypeName = "서비스 정보";
		}
		else if (workType === "AWRK-0004") {
			workTypeName = "정산 정보";
		}
		else if (workType === "AWRK-0005") {
			workTypeName = "충전권";
		}
		else if (workType === "AWRK-0006") {
			workTypeName = "정산내역 조정";
		}
		else if (workType === "AWRK-0007") {
			workTypeName = "경비";
		}
		else if (workType === "AWRK-0008") {
			workTypeName = "정산 수수료 정보";
		}
		else if (workType === "AWRK-0009") {
			workTypeName = "KCON 상품";
		}
		else if (workType === "AWRK-0010") {
			workTypeName = "KCON 쿠폰";
		}
		else if (workType === "AWRK-0011") {
			workTypeName = "카드 잔액환불";
		}
		else if (workType === "AWRK-0012") {
			workTypeName = "카드 사용제한";
		}
		
		return workTypeName;
    }

    this.getApprovalReqType = function(reqType) {
    	
		var reqTypeName = "";
		
		if(reqType === "AREQ-0001") {
			reqTypeName = "등록"
		}
		else if (reqType === "AREQ-0002") {
			reqTypeName = "수정"
		}
		else if (reqType === "AREQ-0003") {
			reqTypeName = "삭제"
		}
		else if (reqType === "AREQ-0004") {
			reqTypeName = "연장"
		}
		else if (reqType === "AREQ-0005") {
			reqTypeName = "사용해제"
		}
		
		return reqTypeName;
    }
	
}


