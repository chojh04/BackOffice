function subMerchantInfo(jsonParam){
	
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
			bodyHtml = subMerchantDetailContent();   				   			
   			buttonHtml ='<button type="button" class="dt-button btn green btn-outline btnAppr">승인처리</button>'
	               +'<button type="button" class="dt-button btn green btn-outline btnReject">반려</button>';
	} else if(status == "ARST-0003" && reqEmpId == empId && typeCode == "APPR-0200"){
		buttonHtml ='<button type="button" class="dt-button btn green btn-outline btnUpt">수정</button>';
		bodyHtml = subMerchantUpdateContent();
	} else{
		bodyHtml = subMerchantDetailContent();
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
	                        url: "/api/approval/submerchant/approvals/approval",
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
		// 사업자번호 중복체크
		,{
			target : ".bzno",
			eventType : "click",
			callBack : function (){
				kpcUtil.bzNoCheck("#merchantUptForm #bizRegNo", "#merchantUptForm");
			}
		}
		// 법인번호 중복체크
	   ,{
			target : ".corpNo",
			eventType : "click",
			callBack : function (){
				kpcUtil.corpNoCheck("#merchantUptForm #corpRegNo", "#merchantUptForm");
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
				
				if($("#submerchantUptForm").valid() && kpcUtil.confirm("수정 후 재승인요청 하시겠습니까?") ){
					var menuId = "MCM-0002";
                	// 승인자 선택
                	kpcPopupUtil.openApprListPop({
                		 menuId : menuId 
                		,callBack : function (data){
                			var updApprEmpId = $("input[name=empList]:checked").attr("empId");
		   					if(typeof updApprEmpId === "undefined"){
		   						kpcUtil.customAlert("승인자를 선택해주세요.");
		   						return false;
		   					} else {
		   						var jsonData = $("#submerchantUptForm").serializeJsonObject();
		   						jsonData["apprEmpId"] = updApprEmpId;
		   						jsonData["menuId"] = menuId;
		   						jsonData["tmpSeq"] = tmpSeq;
		   						jsonData["seq"] = seq;
       		             		$.ajax({
           		         			url: "/api/approval/submerchant/approvals/reject/reApproval",
           		         			data: JSON.stringify(jsonData),
           		         			type:'POST',
           		         			dataType : "json",
           		         			contentType  : "application/json",
       		         			}).done(function (data){
   		                    		if(kpcUtil.successHandlingToMsg("#submerchantUptForm",data,true,"승인 요청 되었습니다.")){
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
                       url: "/api/approval/submerchant/approvals/submerchantTmp",
                       data: "tmpSeq=" + tmpSeq,
                       type:'GET',
                       dataType : "json",
            	}).done(function(resultData,sts,jqXhr){
            		console.log(resultData["apprStatus"]);
            		if(resultData["apprStatus"] == "ARST-0003" && resultData["apprTypeCode"] == "APPR-0200" && reqEmpId == empId){
	   					setSubmerchantUpdDataFormat(resultData);
            		} else {
            			kpcUtil.setFormData("#subMerchantDetailForm" , resultData);
            		}
                }).fail(function(e){
        	    	kpcUtil.errorHandling(e);
      	        });			            			   
    	   }
       }]
	});            		        			
} 


function subMerchantUpdateContent(){
	return''
        +'<div class="form">'
        +'<form action="#" id="submerchantUptForm" class="form-bordered ">'
        +'<input type="hidden" id="parentId" name="parentId" >'
        +'<input type="hidden" id="encAgentPw" name="encAgentPw" >'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
        +'        <label class="control-label col-md-3 col-sm-3 col-xs-12">- 거래처 정보 </label>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">거래처 코드</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'       		<i class="fa"></i>'
        +'            <input type="text" id="submerchantId" name="submerchantId" class="form-control col-md-3 col-xs-12" readonly="readonly">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">거래처 명</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'       		<i class="fa"></i>'
        +'			<input type="text" id="name" name="name" class="form-control col-md-7 col-xs-12 lang-ko"  >'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">거래처약칭</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'       		<i class="fa"></i>'
        +'			<input type="text" id="alias" name="alias" class="form-control col-md-7 col-xs-12">'
        +'        </div>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
        +'        <label class="control-label col-md-3 col-sm-3 col-xs-12">'
        +'        	<span>'
        +'        		<b>[세금계산서 정보]</b>'
        +'        	</span>'
        +'        </label>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12" id="taxDiv">'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표 성명</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'        	<i class="fa"></i>'
        +'            <input type="text" id="ceoNm" name="ceoNm" class="form-control col-md-7 col-xs-12">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">개업일</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">'
        +'            <input type="text" class="form-control input-date-picker" id="openDt" name="openDt" isDateField="true">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">사업자등록번호</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'        	<i class="fa"></i>'
        +'			<input type="text" id="bizRegNo" name="bizRegNo" class="form-control col-md-7 col-xs-12" maxlength="12" isBzno="true">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">법인등록번호</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'        	<i class="fa"></i>'
        +'			<input type="text" id="corpRegNo" name="corpRegNo" class="form-control col-md-7 col-xs-12" maxlength="13">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">업종</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'        	<i class="fa"></i>'
        +'			<input type="text" id="bizKind" name="bizKind" class="form-control col-lg-12 col-md-7 col-xs-12">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">업태</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'        	<i class="fa"></i>'
        +'			<input type="text" id="bizCond" name="bizCond" class="form-control col-lg-12 col-md-7 col-xs-12">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">우편번호</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'        	<i class="fa"></i>'
        +'			<input type="text" id="zipcode" name="zipcode" class="form-control col-md-7 col-xs-12">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">주소</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 input-icon left">'
        +'        	<i class="fa"></i>'
        +'			<input type="text" id="address" name="address" class="form-control col-lg-12 col-md-7 col-xs-12">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12 ">상세주소</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 input-icon left">'
        +'        	<i class="fa"></i>'
        +'			<input type="text" id="addressDtl" name="addressDtl" class="form-control col-lg-12 col-md-7 col-xs-12">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">거래처구분</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">'
        +'            <select class="form-control" id="typeCode" name="typeCode" >'
        +'            </select>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표 연락처</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline ">'
        +'			<input type="text" id="tel" name="tel" class="form-control col-md-7 col-xs-12" isTel="true">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표 팩스번호</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">'
        +'			<input type="text" id="fax" name="fax" class="form-control col-md-7 col-xs-12" isTel="true">'
        +'        </div>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
        +'        <label class="control-label col-md-3 col-sm-3 col-xs-12"><b>[전자세금계산서 발행정보]</b></label>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12" >'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">세금계산서 담당자</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'        	<i class="fa"></i>'
        +'			<input type="text" id="taxCustNm" name="taxCustNm" class="form-control col-md-7 col-xs-12">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">전화번호</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">'
        +'			<input type="text" id="taxTel" name="taxTel" class="form-control col-md-7 col-xs-12" isTel="true">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">팩스번호</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">'
        +'			<input type="text" id="taxFax" name="taxFax" class="form-control col-md-7 col-xs-12" isTel="true">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">핸드폰번호</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">'
        +'			<input type="text" id="taxPhone" name="taxPhone" class="form-control col-md-7 col-xs-12" isTel="true">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">E-MAIL</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'        	<i class="fa"></i>'
        +'			<input type="text" id="taxEmail" name="taxEmail" class="form-control col-lg-12 col-lg-7 col-xs-12">'
        +'        </div>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
        +'        <label class="control-label col-md-3 col-sm-3 col-xs-12"><b>[계좌정보]</b></label>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">은행</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'        	<i class="fa"></i>'
		+'             <select class="form-control isSelectValid" id="bankNm" name="bankNm">'
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
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">영업담당자</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline ">'
        +'			<input type="text" id="salesNm" name="salesNm" class="form-control col-md-7 col-xs-12">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">영업담당자 연락처</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">'
        +'			<input type="text" id="salesTel" name="salesTel" class="form-control col-md-7 col-xs-12" isTel="true">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline ">'
        +'			<input type="text" id="billingNm" name="billingNm" class="form-control col-md-7 col-xs-12">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자 연락처</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">'
        +'			<input type="text" id="billingTel" name="billingTel" class="form-control col-md-7 col-xs-12" isTel="true">'
        +'        </div>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
        +'        <label class="control-label col-md-3 col-sm-3 col-xs-12">[KPC 담당자정보]</label>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">영업담당자</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline ">'
        +'			<input type="text" id="kpcSalesNm" name="kpcSalesNm" class="form-control col-md-7 col-xs-12">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">영업담당자 연락처</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">'
        +'			<input type="text" id="kpcSalesTel" name="kpcSalesTel" class="form-control col-md-7 col-xs-12" isTel="true">'
        +'        </div>'
        +'    </div>'
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
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
        +'        <label class="control-label col-md-3 col-sm-3 col-xs-12"><b>[연동정보]</b></label>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">에이전트 아이디</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'        	<i class="fa"></i>'
        +'			<input type="text" id="agentId" name="agentId" class="form-control col-md-7 col-xs-12">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">에이전트 비밀번호</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'        	<i class="fa"></i>'
        +'			<input type="password" id="agentPw" name="agentPw" class="form-control col-md-7 col-xs-12">'
        +'        </div>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
        +'        <label class="control-label col-md-3 col-sm-3 col-xs-12"><b>[기타정보]</b></label>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">사용여부</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">'
        +'            <select class="form-control" id="useFlag" name="useFlag" >'
        +'            	<option value="Y">사용</option>'
        +'            	<option value="N">미사용</option>'
        +'            </select>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">홈페이지 URL</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">'
        +'			<input type="text" id="urlHome" name="urlHome" class="form-control col-lg-12 col-md-12 col-xs-12">'
        +'        </div>'
        +'    </div>'
        +'</div>'        
        +'</form>'
        +'</div><br />';            	
}

function subMerchantDetailContent(){
 	 return'<br />'
         +'<form action="#" id="subMerchantDetailForm" class="form-bordered ">'
         +' 	<input type="hidden" id="path" name="path" >'
         +'     <div class="col-md-12 col-sm-12 col-xs-12">'
         +'         <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
         +'             <label class="control-label col-md-12 col-sm-3 col-xs-12">- 거래처 정보 </label>'
         +'         </div>'
         +'     </div>'
         +'     <div class="col-md-12 col-sm-12 col-xs-12">'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">상위거래처 코드</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12  form-border-left-lg">'
         +'                 <span id="parentId" class="span-vertical-middle col-md-12 col-xs-12" ></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">상위거래처 명</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12  form-border-left-lg">'
         +'                 <span id="parentNm" class="span-vertical-middle col-md-12 col-xs-12" ></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">거래처코드</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12  form-border-left-lg">'
         +'                 <span id="submerchantId" class="span-vertical-middle col-md-12 col-xs-12" ></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">거래처 명</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +' 				<span id="name" class="span-vertical-middle col-md-7 col-xs-12"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">거래처약칭</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +' 				<span id="alias" class="span-vertical-middle col-md-7 col-xs-12"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표성명</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +' 				<span id="ceoNm" class="span-vertical-middle col-md-7 col-xs-12"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">개업일</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +' 				<span id="openDt" class="span-vertical-middle col-md-7 col-xs-12" isDateField="true"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">사업자번호</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +' 				<span id="bizRegNo" class="span-vertical-middle col-md-7 col-xs-12" isBzno="true"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">법인등록번호</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +' 				<span id="corpRegNo" class="span-vertical-middle col-md-7 col-xs-12"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">업종</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +'                 <span class="span-vertical-middle col-md-7 col-xs-12" id="bizKind" ></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">업태</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +'                 <span class="span-vertical-middle col-md-7 col-xs-12" id="bizCond" ></span>    							'			
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">우편번호</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12  form-border-left-lg">'
         +'                 <span id="zipcode" class="span-vertical-middle col-md-7 col-xs-12"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">주소</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +'                 <span id="address" class="span-vertical-middle col-md-7 col-xs-12"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">상세주소</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +'                 <span id="addressDtl" class="span-vertical-middle col-md-7 col-xs-12"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표연락처</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +'                 <span id="tel" class="span-vertical-middle col-md-7 col-xs-12" isTel="true"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표팩스번호</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +'                 <span id="fax" class="span-vertical-middle col-md-7 col-xs-12" isTel="true"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">세금계산서 담당자</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +'                 <span id="taxCustNm" class="span-vertical-middle col-md-7 col-xs-12"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">세금계산서 발행 E-MAIL</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +'                 <span id="taxEmail" class="span-vertical-middle col-md-7 col-xs-12"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">전화번호</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +'                 <span id="taxTel" class="span-vertical-middle col-md-7 col-xs-12" isTel="true"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">팩스번호</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +'                 <span id="taxFax" class="span-vertical-middle col-md-7 col-xs-12" isTel="true"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">핸드폰번호</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +'                 <span id="taxPhone" class="span-vertical-middle col-md-7 col-xs-12" isTel="true"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">사용여부</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +'                 <span id="useFlagNm" class="span-vertical-middle col-md-7 col-xs-12"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">영업담당자</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +'                 <span id="salesNm" class="span-vertical-middle col-md-7 col-xs-12"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">영업담당자 연락처</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +'                 <span id="salesTel" class="span-vertical-middle col-md-7 col-xs-12" isTel="true"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +'                 <span id="billingNm" class="span-vertical-middle col-md-7 col-xs-12"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자 연락처</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +'                 <span id="billingTel" class="span-vertical-middle col-md-7 col-xs-12" isTel="true"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">KPC영업담당자</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +'                 <span id="kpcSalesNm" class="span-vertical-middle col-md-7 col-xs-12"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">KPC영업담당자 연락처</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +'                 <span id="kpcSalesTel" class="span-vertical-middle col-md-7 col-xs-12" isTel="true"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">KPC정산담당자</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +'                 <span id="kpcBillingNm" class="span-vertical-middle col-md-7 col-xs-12"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">KPC정산담당자 연락처</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +'                 <span id="kpcBillingTel" class="span-vertical-middle col-md-7 col-xs-12" isTel="true"></span>'
         +'             </div>'
         +'         </div>'
         +'         <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
         +'             <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">에이전트 아이디</label>'
         +'             <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
         +'                 <span id="agentId" class="span-vertical-middle col-md-7 col-xs-12"></span>'
         +'             </div>'
         +'         </div>'
         +'     </div>'
         +' </form>'
          ;
}


function setSubmerchantUpdDataFormat(merchantData){
    $("#submerchantUptForm #useFlag").select2({
        width: 110,
    });    	
    kpcUtil.setDatePicker('#submerchantUptForm #openDt');
	kpcUtil.setSelectBoxData({
		target : [
		          "#submerchantUptForm #typeCode",
		          "#submerchantUptForm #bankNm",
		], 
		apiUrl : "/api/systemMng/common/commonCodeList",
		params : {type : 'MER,BANK'},
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
        	kpcUtil.setFormData("#submerchantUptForm" , merchantData)
			$("#submerchantUptForm #encAgentPw").val($("#submerchantUptForm #agentPw").val());
        	setSubFormValidate();
        	$("#submerchantUptForm").valid();
			kpcUtil.setFormTextFieldFormat({
				target : "#submerchantUptForm"
			});
		}
	});                
}

var setSubFormValidate = function (){
    $("#submerchantUptForm").validate({
        errorElement: 'span', //default input error message container
        errorClass: 'help-block help-block-error', // default input error message class
        rules: {
        	name : {
                required : true,
            },
        	alias : {
                required : true,
            },
            bizKind : {
                required : true,
            },
            bizCond : {
                required : true,
            },
            typeCode : {	
                required : true,
            },
            ceoName : {
                required : true,
            },
            zipcode : {
                required : true,
            },
            address : {
                required : true,
            },
            addressDetail : {
                required : true,
            },
            tel : {
                required : true,
            },
            taxCustNm : {
                required : true,
            },
            taxEmail : {
                required : true,
            },
            bankCd : {
                required : true,
            },
            bankAccNo : {
                required : true,
            },
            bankHolder : {
                required : true,
            },
            agentId : {
                required : true,
            },
            agentPw : {
                required : true,
            },
        },
        messages : {
        	name : {
                required : "대표 거래처명을 입력해주세요.",
            },
            bizKind : {
                required : "업종을 선택해주세요.",
            },
            bizCond : {
                required : "업태를 선택해주세요.",
            },
            typeCode : {	
                required : "가맹점 구분을 선택해주세요.",
            },
            ceoName : {
                required : "대표 성명을 입력해주세요.",
            },
            zipcode : {
                required : "우편 번호를 입력해주세요.",
            },
            address : {
                required : "주소를 입력해주세요.",
            },
            addressDetail : {
                required : "상세주소를 입력해주세요.",
            },
            tel : {
                required : "비밀번호를 입력해주세요.",
            },
            taxCustNm : {
                required : "세금계산서 담당자를 입력해주세요.",
            },
            taxEmail : {
                required : "Email을 입력해주세요.",
            },                        
            telSub : {
                required : "대표 연락처를 입력해주세요.",
            },
            bankCd : {
                required : "은행명을 선택해주세요.",
            },
            bankAccNo : {
                required : "계좌번호를 입력해주세요.",
            },
            bankHolder : {
                required : "예금주를 입력해주세요.",
            },
            agentId : {
                required : "에이전트 아이디를 입력해주세요.",
            },
            agentPw : {
                required : "에이전트 비밀번호를 입력해주세요.",
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
    
	// TODO : bootstrap select2의 경우 jquery validate의 change이벤트가 적용안됨 수정적용
	$("#submerchantUptForm .isSelectValid").on("change" , function (){
		$(this).valid();
	});	        

}