function billingInfo(jsonParam){
	
	var seq       = jsonParam.seq;
	var tmpSeq    = jsonParam.tmpSeq;
	var status    = jsonParam.status;
	var reqEmpId  = jsonParam.reqEmpId;
	var apprEmpId = jsonParam.apprEmpId;
	var typeCode  = jsonParam.typeCode;            	
	var empId     = jsonParam.empId;            	
	var table     = jsonParam.table;            	

	var buttonHtml ='';
	var bodyHtml ='';
	if(status == "ARST-0001"&& apprEmpId == empId){
			bodyHtml = billingDetailContent();   				   			
   			buttonHtml ='<button type="button" class="dt-button btn green btn-outline btnAppr">승인처리</button>'
	               +'<button type="button" class="dt-button btn green btn-outline btnReject">반려</button>';
	} else if(status == "ARST-0003" && reqEmpId == empId && typeCode == "APPR-0400"){
		buttonHtml ='<button type="button" class="dt-button btn green btn-outline btnUpt">수정</button>';
		bodyHtml = billingUpdateContent();
	} else{
		bodyHtml = billingDetailContent();
	}
	kpcUtil.openCommonPopup({
		modalTitle : "상세 정보",
		bodyHtml : bodyHtml,
		button : buttonHtml,
		modalSize : "modal-xlg",
		buttonEvent : [{
			target : ".btnAppr",
			eventType : "click",
			callBack : function (){
				if(kpcUtil.confirm("승인 하시겠습니까?")){
					try{
   						$.ajax({
	                        url: "/api/approval/billing/approvals/approval",
	                        data: JSON.stringify({"seq" : seq , "tmpSeq" : tmpSeq , "typeCode" : typeCode}),
	                        type:'POST',
	                        dataType : "json",
	                        contentType  : "application/json",
	                    }).done(function(resultData,status,jqXhr){
	                    	if(kpcUtil.successHandlingToMsg("",resultData,false,"승인 되었습니다.")){
	                    		$(".modal").modal("toggle");
	                    		table.fnFilter();
	                    	}
	                    }).fail(function(e){
	                		kpcUtil.errorHandling(e);
	              	    });
					} catch(e){
						kpcUtil.customAlert("Google Chrome 이용 바랍니다.");
					}
				}
			}
		}
	   ,{
			target : ".btnReject",
			eventType : "click",
			callBack : function (){
				
				kpcPopupUtil.openPromptPop({
					confirmMsg : "반려 사유를 입력해주세요."
				   ,confirmTitle : "반려"
				   ,promptCallback : function (desc){
   						$.ajax({
	                        url: "/api/approval/reject",
	                        data: JSON.stringify({"seq" : seq , "tmpSeq" : tmpSeq , "desc" : desc}),
	                        type:'POST',
	                        dataType : "json",
	                        contentType  : "application/json",
	                    }).done(function(data,status,jqXhr){
	                    	if(kpcUtil.successHandlingToMsg("",data,false,"반려 처리 되었습니다.")){
	                    		$(".modal").modal("toggle");
	                    		table.fnFilter();
	                    	}
	                    }).fail(function(e){
	                		kpcUtil.errorHandling(e);
	              	    });				   						   
				   }
				});
				

			}
		}
	   ,{
			target : ".btnUpt",
			eventType : "click",
			callBack : function (){
				
				if($("#billingUptForm").valid() && kpcUtil.confirm("수정 후 재승인요청 하시겠습니까?") ){
					var menuId = "MCM-0003";
                	// 승인자 선택
                	kpcPopupUtil.openApprListPop({
                		 menuId : menuId 
                		,callBack : function (data){
                			var updApprEmpId = $("input[name=empList]:checked").attr("empId");
		   					if(typeof updApprEmpId === "undefined"){
		   						kpcUtil.customAlert("승인자를 선택해주세요.");
		   						return false;
		   					} else {
		   						var jsonData = $("#billingUptForm").serializeJsonObject();
		   						jsonData["apprEmpId"] = updApprEmpId;
		   						jsonData["menuId"] = menuId;
		   						jsonData["tmpSeq"] = tmpSeq;
		   						jsonData["seq"] = seq;
       		             		$.ajax({
           		         			url: "/api/approval/billing/approvals/reject/reApproval",
           		         			data: JSON.stringify(jsonData),
           		         			type:'POST',
           		         			dataType : "json",
           		         			contentType  : "application/json",
       		         			}).done(function (data){
   		                    		if(kpcUtil.successHandlingToMsg("#billingUptForm",data,true,"승인 요청 되었습니다.")){
   		                    			$(".modal").modal('toggle');
   		                    			table.fnFilter();
   		                    		}           		       		                        	
       		         			}).fail(function (e){
       		         				kpcUtil.errorHandling(e);
       		         			});              		   			   						
		   						
		   					}
                		}
                	});           		                    	
                	
				}
			}
		}		   		   
       ,{
    	   target : ".modal",
    	   eventType : "shown.bs.modal",
    	   callBack : function (){
                $.ajax({
                       url: "/api/approval/billing/approvals/billingTmp",
                       data: "tmpSeq=" + tmpSeq,
                       type:'GET',
                       dataType : "json",
            	}).done(function(resultData,sts,jqXhr){
            		if(resultData["apprStatus"] == "ARST-0003" && resultData["apprTypeCode"] == "APPR-0400" && reqEmpId == empId){
            			setBillingUpdDataFormat(resultData);
            		} else {
            			console.log(resultData);
            			kpcUtil.setFormData("#billingDetailPopupForm" , resultData);       			
            		}
                }).fail(function(e){
        	    	kpcUtil.errorHandling(e);
      	        });			            			   
    	   }
       }]
	});            		        			
}		

function billingDetailContent(){
	return'<div class="col-md-12 col-sm-12 col-xs-12">'
		+'    <div class="form">'
		+'        <form action="#" id="billingDetailPopupForm" class="form-bordered ">'
		+'            <input type="hidden" id="serviceId" name="serviceId">'
		+'            <div class="col-md-12 col-sm-12 col-xs-12">'
		+'                <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
		+'                    <label class="control-label col-md-3 col-sm-3 col-xs-12">- 정산정보 </label>'
		+'                </div>'
		+'            </div>'
		+'            <div class="col-md-12 col-sm-12 col-xs-12">'
		+'                <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
		+'                    <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산코드</label>'
		+'                    <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg ">'
		+'                        <span  id="serviceBillingId" class="span-vertical-middle col-md-7 col-xs-12"  ></span>'
		+'                    </div>'
		+'                </div>'
		+'                <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
		+'                    <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산명</label>'
		+'                    <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg ">'
		+'						<span  id="name" class="span-vertical-middle col-md-7 col-xs-12"></span>'
		+'                    </div>'
		+'                </div>'
		+'            </div>'
		+'            <div class="col-md-12 col-sm-12 col-xs-12">'
		+'                <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
		+'                    <label class="control-label col-md-3 col-sm-3 col-xs-12">'
		+'                    	<span>'
		+'                    		<b>[계좌정보]</b>'
		+'                    	</span>'
		+'                    </label>'
		+'                </div>'
		+'            </div>'
		+'            <div class="col-md-12 col-sm-12 col-xs-12" id="accDiv">'
		+'                <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
		+'                    <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">은행명</label>'
		+'                    <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg ">'
		+'                    	'
		+'						<span  id="bankNm" class="span-vertical-middle col-md-7 col-xs-12"></span>'
		+'                    </div>'
		+'                </div>'
		+'                <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
		+'                    <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12 ">계좌번호</label>'
		+'                    <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg ">'
		+'                    	'
		+'						<span  id="bankAccNo"  class="span-vertical-middle col-md-7 col-xs-12"></span>'
		+'                    </div>'
		+'                </div>'
		+'                <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
		+'                    <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">예금주</label>'
		+'                    <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg ">'
		+'                    	'
		+'						<span  id="bankHolder" class="span-vertical-middle col-md-7 col-xs-12"></span>'
		+'                    </div>'
		+'                </div>'
		+'            </div>'
		+'            <div class="col-md-12 col-sm-12 col-xs-12">'
		+'                <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
		+'                    <label class="control-label col-md-3 col-sm-3 col-xs-12"><b>[거래처 담당자정보]</b></label>'
		+'                </div>'
		+'            </div>'
		+'            <div class="col-md-12 col-sm-12 col-xs-12">'
		+'                <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
		+'                    <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자</label>'
		+'                    <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg ">'
		+'						<span  id="billingNm" class="span-vertical-middle col-md-7 col-xs-12"></span>'
		+'                    </div>'
		+'                </div>'
		+'                <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
		+'                    <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자 연락처</label>'
		+'                    <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
		+'						<span  id="billingTel" class="span-vertical-middle col-md-7 col-xs-12" isTel="true"></span>'
		+'                    </div>'
		+'                </div>'
		+'                <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
		+'                    <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자 이메일</label>'
		+'                    <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg ">'
		+'						<span  id="billingEmail" class="span-vertical-middle col-md-7 col-xs-12"></span>'
		+'                    </div>'
		+'                </div>'
		+'            </div>'
		+'            <div class="col-md-12 col-sm-12 col-xs-12">'
		+'                <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
		+'                    <label class="control-label col-md-3 col-sm-3 col-xs-12"><b>[KPC 담당자정보]</b></label>'
		+'                </div>'
		+'            </div>'
		+'            <div class="col-md-12 col-sm-12 col-xs-12">'
		+'                <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
		+'                    <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자</label>'
		+'                    <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg ">'
		+'						<span  id="kpcBillingNm"  class="span-vertical-middle col-md-7 col-xs-12" ></span>'
		+'                    </div>'
		+'                </div>'
		+'                <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
		+'                    <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자 연락처</label>'
		+'                    <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
		+'						<span  id="kpcBillingTel" class="span-vertical-middle col-md-7 col-xs-12" isTel="true"></span>'
		+'                    </div>'
		+'                </div>'
		+'                <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
		+'                    <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자 이메일</label>'
		+'                    <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg ">'
		+'						<span  id="kpcBillingEmail" class="span-vertical-middle col-md-7 col-xs-12" ></span>'
		+'                    </div>'
		+'                </div>'
		+'            </div>'
		+'            <div class="col-md-12 col-sm-12 col-xs-12">'
		+'                <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
		+'                    <label class="control-label col-md-3 col-sm-3 col-xs-12"><b>[정산정보]</b></label>'
		+'                </div>'
		+'            </div>'
		+'            <div class="col-md-12 col-sm-12 col-xs-12">'
		+'                <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
		+'                    <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">거래구분</label>'
		+'                    <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg ">'
		+'                        <span  id="dividerName" class="span-vertical-middle col-md-7 col-xs-12"></span>'
		+'                    </div>'
		+'                </div>'
		+'                <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
		+'                    <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산 구분</label>'
		+'                    <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
		+'                        <span  id="codeName" class="span-vertical-middle col-md-7 col-xs-12"></span>'
		+'                    </div>'
		+'                </div>'
		+'                <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
		+'                    <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산주기</label>'
		+'                    <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg ">'
		+'                        <span  id="billingDurationName" class="span-vertical-middle col-md-7 col-xs-12"></span>'
		+'                    </div>'
		+'                </div>'
		+'                <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
		+'                    <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산일</label>'
		+'                    <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
		+'						<span  id="billingDt"  class="span-vertical-middle col-md-7 col-xs-12"></span>'
		+'                    </div>'
		+'                </div>'
		+'                <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
		+'                    <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">부가세 타입</label>'
		+'                    <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg ">'
		+'						<span  id="merchantTaxTypeName"  class="span-vertical-middle col-md-7 col-xs-12"></span>'
		+'                    </div>'
		+'                </div>'
		+'                <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
		+'                    <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">수수료 타입</label>'
		+'                    <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
		+'						<span  id="merchantCommTypeName" class="span-vertical-middle col-md-7 col-xs-12"></span>'
		+'                    </div>'
		+'                </div>'
		+'                <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
		+'                    <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">수수료</label>'
		+'                    <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg ">'
		+'                        <span  id="merchantCommisionName" class="span-vertical-middle col-md-7 col-xs-12"></span>'
		+'                    </div>'
		+'                </div>'
		+'                <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
		+'                    <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">수수료 변경 예정일</label>'
		+'                    <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg ">'
		+'                        <span  id="aplEndDt" class="span-vertical-middle col-md-7 col-xs-12"></span>'
		+'                    </div>'
		+'                </div>'
		+'            </div>'
		+'        </form>'
		+'    </div>'
		+'</div>';
}                                                                                                                                    

function billingUpdateContent(serviceBillingId,callback){
	return''
        +'<div class="form">'                                                                                                                          
        +'<form action="#" id="billingUptForm" class="form-bordered ">'                                                                                
        +'<input type="hidden" id="serviceId" name="serviceId">'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
        +'        <label class="control-label col-md-3 col-sm-3 col-xs-12">- 정산정보 </label>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산코드</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'       		<i class="fa"></i>'
        +'            <input type="text" id="serviceBillingId" name="serviceBillingId" class="form-control col-md-3 col-xs-12" readonly="readonly">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산명</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'        	<i class="fa"></i>'
		+'			<input type="text" id="name" name="name" class="form-control col-md-7 col-xs-12">'
        +'        </div>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
        +'        <label class="control-label col-md-3 col-sm-3 col-xs-12">'
        +'        	<span>'
        +'        		<b>[계좌정보]</b>'
        +'        	</span>'
        +'        </label>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12" id="accDiv">'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">은행명</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'        	<i class="fa"></i>'
		+'             <select class="form-control isSelectValid" id="bankCd" name="bankCd">'
		+'                 <option value="">선택</option>'
        +'             </select>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12 input-icon left">계좌번호</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'        	<i class="fa"></i>'
		+'			<input type="text" id="bankAccNo" name="bankAccNo" class="form-control col-md-7 col-xs-12">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">예금주</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'        	<i class="fa"></i>'
		+'			<input type="text" id="bankHolder" name="bankHolder" class="form-control col-md-7 col-xs-12">'
        +'        </div>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
        +'        <label class="control-label col-md-3 col-sm-3 col-xs-12"><b>[거래처 담당자정보]</b></label>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'        	<i class="fa"></i>'
		+'			<input type="text" id="billingNm" name="billingNm" class="form-control col-md-7 col-xs-12">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자 연락처</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">'
		+'			<input type="text" id="billingTel" name="billingTel" class="form-control col-md-7 col-xs-12" isTel="true">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자 이메일</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'        	<i class="fa"></i>'
		+'			<input type="text" id="billingEmail" name="billingEmail" class="form-control col-md-7 col-xs-12">'
        +'        </div>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
        +'        <label class="control-label col-md-3 col-sm-3 col-xs-12"><b>[KPC 담당자정보]</b></label>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline ">'
		+'			<input type="text" id="kpcBillingNm" name="kpcBillingNm" class="form-control col-md-7 col-xs-12">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자 연락처</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">'
		+'			<input type="text" id="kpcBillingTel" name="kpcBillingTel" class="form-control col-md-7 col-xs-12" isTel="true">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자 이메일</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline ">'
		+'			<input type="text" id="kpcBillingEmail" name="kpcBillingEmail" class="form-control col-md-7 col-xs-12" >'
        +'        </div>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
        +'        <label class="control-label col-md-3 col-sm-3 col-xs-12"><b>[정산정보]</b></label>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">거래구분</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline ">'
        +'            <select class="form-control" id="divider" name="divider" >'
        +'            </select>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산 구분</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">'
        +'            <select class="form-control" id="code" name="code" >'
        +'            </select>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산주기</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline ">'
        +'            <select class="form-control" id="billingDuration" name="billingDuration" >'
        +'            </select>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산일</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline custom-input-icon left">'
		+'			<i>D+</i>'
		+'			<input type="text" id="billingDt" name="billingDt" class=" col-lg-3 col-md-5 col-xs-12" >'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">부가세 타입</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline ">'
        +'			<select class="form-control" id="merchantTaxType" name="merchantTaxType" >'
        +'            </select>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">수수료 타입</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">'
        +'			<select class="form-control" id="merchantCommType" name="merchantCommType" >'
        +'            </select>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">수수료</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left ">'
        +'        <i class="fa"></i>'
        +'            <input type="text" id="merchantCommision" name="merchantCommision" class="form-control input-xsmall">'
        +'        </div>'
        +'    </div>'
        +'</div>'
        +'</form>'                                                                                                                                     
        +'</div><br />';
}

function setBillingUpdDataFormat(billingData){
	kpcUtil.setDatePicker("#billingUptForm #aplEndDate");
	setBillingFormValidate();
	kpcUtil.setSelectBoxData({
		target : [
		          "#billingUptForm #divider",
		          "#billingUptForm #code", 
		          "#billingUptForm #billingDuration",
		          "#billingUptForm #merchantCommType", 
		          "#billingUptForm #merchantTaxType", 
		          "#billingUptForm #bankCd", 
		], 
		apiUrl : "/api/systemMng/common/commonCodeList",
		params : {type : 'DEAL,BIL,BILC,FEE,TAX,BANK'},
		type   : "GET",
		option : {width : 150},	
		callBack : function (data,target,option){
			for(var idx in data){
				for(var idx2 in data[idx].resultList){
    				$(target[idx]).append($("<option></option>")
    						.attr("value" , data[idx].resultList[idx2].code)
    						.text(data[idx].resultList[idx2].codeName));
				}
				$(target[idx]).select2(option);       
			}
	    	kpcUtil.setFormData("#billingUptForm" , billingData);
	    	$("#billingUptForm").valid();
			kpcUtil.setFormTextFieldFormat({
				target : "#billingUptForm"
			});			    	
		}
	});		
}

function setBillingFormValidate(){
    $("#billingUptForm").validate({
        errorElement: 'span', //default input error message container
        errorClass: 'help-block help-block-error', // default input error message class
        rules: {
        	serviceId : {
        		required : true,
            },
        	name : {
        		required : true,
            },
            bankCd: {
        		required : true,
            },
            bankAccNo: {
        		required : true,
            },
            bankHolder: {
        		required : true,
            },
            billingNm: {
        		required : true,
            },
            billingEmail: {
        		required : true,
            },
            merchantCommision: {
            	number : true,
            },
        },
        messages : {
        	serviceId : {
        		required : "서비스코드가 없습니다.",
            },
            name : {
            	required : "정산명을 입력해주세요.",
            },
            bankCd: {
        		required : "은행명을 선택해주세요.",
            },
            bankAccNo: {
        		required : "계좌번호를 입력해주세요.",
            },
            bankHolder: {
        		required : "예금주를 입력해주세요.",
            },
            billingNm: {
        		required : "정산담당자를 입력해주세요.",
            },
            billingEmail: {
        		required : "정산담당자 이메일을 입력해주세요.",
            },                      
            merchantCommision: {
            	number : "숫자만 입력해주세요."
            },                      
        },
        invalidHandler:function (form,validator){
        	if(validator.numberOfInvalids()){
        		kpcUtil.customAlert("필수항목이 입력되지 않았습니다.");
        	}
        },        
        errorPlacement : function (error , element){
        	var icon = $(element).parent(".input-icon").children('i');
        	icon.removeClass('fa-check').addClass("fa-warning");
        	icon.attr("data-original-title" , error.text()).tooltip({"container" : "body"});
        },
        highlight: function (element) { // hightlight error inputs
           	$(element).closest('.form-group').addClass('has-error'); // set error class to the control group
        },
        success : function (label,element){
        	var icon = $(element).parent(".input-icon").children('i');
        	$(element).closest(".form-group").removeClass("has-error").addClass("has-success");
        	icon.removeClass('fa-warning').addClass("fa-check");
        },
    });
	
	// TODO :  bootstrap select2의 경우 jquery validate의 change이벤트가 적용안됨 수정적용
	$("#billingUptForm .isSelectValid").on("change" , function (){
		$(this).valid();
	});	    

}