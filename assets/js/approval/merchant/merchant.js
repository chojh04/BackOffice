function merchantInfo(jsonParam){
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
			bodyHtml = merchantDetailContent();   				   			
			buttonHtml ='<button type="button" class="dt-button btn green btn-outline btnAppr">승인처리</button>'
	               +'<button type="button" class="dt-button btn green btn-outline btnReject">반려</button>';
	} else if(status == "ARST-0003" && reqEmpId == empId && typeCode == "APPR-0100"){
		buttonHtml ='<button type="button" class="dt-button btn green btn-outline btnUpt">수정</button>';
	  		bodyHtml = merchantUpdateContent();
	} else{
		bodyHtml = merchantDetailContent();
	}
	kpcUtil.openCommonPopup({
		modalTitle : "상세 정보",
		bodyHtml : bodyHtml,
		button : buttonHtml,
		modalSize : "modal-full",
		buttonEvent : [{
			target : ".btnAppr",
			eventType : "click",
			callBack : function (){
				if(kpcUtil.confirm("승인 하시겠습니까?")){
					try{
						$.ajax({
	                        url: "/api/approval/merchant/approvals/approval",
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
				
				if($("#merchantUptForm").valid() && kpcUtil.confirm("수정 후 재승인요청 하시겠습니까?") ){
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
		   						var jsonData = $("#merchantUptForm").serializeJsonObject();
		   						jsonData["apprEmpId"] = updApprEmpId;
		   						jsonData["menuId"] = menuId;
		   						jsonData["tmpSeq"] = tmpSeq;
		   						jsonData["seq"] = seq;
	      		             		$.ajax({
	       		         			url: "/api/approval/merchant/approvals/reject/reApproval",
	       		         			data: JSON.stringify(jsonData),
	       		         			type:'POST',
	       		         			dataType : "json",
	       		         			contentType  : "application/json",
	      		         			}).done(function (data){
	  		                    		if(kpcUtil.successHandlingToMsg("#merchantUptForm",data,true,"승인 요청 되었습니다.")){
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
	                      url: "/api/approval/merchant/approvals/merchantTmp",
	                      data: "tmpSeq=" + tmpSeq,
	                      type:'GET',
	                      dataType : "json",
	              	}).done(function(resultData,sts,jqXhr){
	              		if(resultData["apprStatus"] == "ARST-0003" && resultData["apprTypeCode"] == "APPR-0100" && reqEmpId == empId){
	  	   					setUpdDataFormat(resultData);
	              		} else {
	              			kpcUtil.setFormData("#detailForm" , resultData);
	              		}
	                }).fail(function(e){
	          	    	kpcUtil.errorHandling(e);
        	        });			            			   
	      	   }
	         }]
	});            		        			
}

function merchantDetailContent(){
	 return'<br />'
        +'<form action="#" id="detailForm" class="form-bordered ">'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
        +'        <label class="control-label col-md-3 col-sm-3 col-xs-12">- 대표 거래처 정보 </label>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표 거래처 코드</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12  form-border-left-lg" >'
        +'            <span id="merchantId" class=" col-md-3 col-xs-12 span-vertical-middle"></span>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표 거래처 명</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12  form-border-left-lg" >'
	     +'				<span id="name" class=" col-md-7 col-xs-12 span-vertical-middle"></span>'
        +'        </div>'
        +'    </div>'
        +'</div>'
        
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
        +'        <label class="control-label col-md-3 col-sm-3 col-xs-12">- 세금 계산서 정보 </label>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표 성명</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12  form-border-left-lg">'
        +'            <span id="ceoNm" class=" col-md-7 col-xs-12 span-vertical-middle"></span>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">개업일</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
        +'            <span class=" col-lg-12 col-md-7 col-xs-12 span-vertical-middle" id="openDt" isDateField="true"></span>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">사업자 번호</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12  form-border-left-lg">'
	     +'				<span id="bizRegNo" class=" col-md-7 col-xs-12 span-vertical-middle" isBzno="true"></span>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">법인등록번호</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12  form-border-left-lg">'
	     +'				<span id="corpRegNo" class=" col-md-7 col-xs-12 span-vertical-middle" ></span>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">업종</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
        +'            <span class=" col-lg-12 col-md-7 col-xs-12 span-vertical-middle" id="bizKind" ></span>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">업태</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
        +'            <span class=" col-lg-12 col-md-7 col-xs-12 span-vertical-middle" id="bizCond" ></span>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">우편번호</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12  form-border-left-lg">'
	     +'				<span id="zipcode" class=" col-lg-12 col-md-7 col-xs-12 span-vertical-middle"></span>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">주소</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
	     +'				<span id="address" class=" col-lg-12 col-md-7 col-xs-12 span-vertical-middle"></span>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">상세주소</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
	     +'				<span id="addressDtl" class=" col-lg-12 col-md-7 col-xs-12 span-vertical-middle"></span>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">거래처구분</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
        +'            <span class=" col-lg-12 col-md-7 col-xs-12 span-vertical-middle" id="bizGrpNm" ></span>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표 연락처</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12  form-border-left-lg">'
	     +'				<span id="tel"  class=" col-md-7 col-xs-12 span-vertical-middle" isTel="true"></span>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표 팩스번호</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
	     +'				<span id="fax" class=" col-md-7 col-xs-12 span-vertical-middle" isTel="true"></span>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">사용여부</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12  form-border-left-lg">'
        +'            <span id="useFlagName" class=" col-md-7 col-xs-12 span-vertical-middle"></span>'
        +'        </div>'
        +'    </div>'
        +'</div>'
        +'</form>'
	 ;            	
}
function merchantUpdateContent(){
	return''
       +'<div class="form">'
       +'    <form action="#" id="merchantUptForm" class="form-bordered ">'
       +'        <div class="col-md-12 col-sm-12 col-xs-12">'
       +'            <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
       +'                <label class="control-label col-md-3 col-sm-3 col-xs-12">- 대표 거래처 등록 </label>'
       +'            </div>'
       +'        </div>'
       +'        <div class="col-md-12 col-sm-12 col-xs-12">'
       +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
       +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표 거래처 코드</label>'
       +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
       +'               		<i class="fa"></i>'
       +'                    <input type="text" id="merchantId" name="merchantId" class="form-control col-md-3 col-xs-12" readonly="readonly">'
       +'                </div>'
       +'            </div>'
       +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
       +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표 거래처 명</label>'
       +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
       +'               		<i class="fa"></i>'
	    +'					<input type="text" id="name" name="name" class="form-control col-md-7 col-xs-12">'
       +'                </div>'
       +'            </div>'
       +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
       +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표 거래처 약칭</label>'
       +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">'
       +'                    <input type="text" id="alias" name="alias" class="form-control col-md-7 col-xs-12">'
       +'                </div>'
       +'            </div>'
       +'        </div>'
       +'        <div class="col-md-12 col-sm-12 col-xs-12">'
       +'            <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
       +'                <label class="control-label col-md-3 col-sm-3 col-xs-12"><b>[세금계산서 정보]</b></label>'
       +'            </div>'
       +'        </div>'
       +'        <div class="col-md-12 col-sm-12 col-xs-12">'
       +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
       +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표 성명</label>'
       +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
       +'                	<i class="fa"></i>'
       +'                    <input type="text" id="ceoNm" name="ceoNm" class="form-control col-md-7 col-xs-12">'
       +'                </div>'
       +'            </div>'
       +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
       +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">개업일</label>'
       +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">'
       +'                    <input type="text" class="form-control input-date-picker" id="openDt" name="openDt" isDateField="true">'
       +'                </div>'
       +'            </div>'
       +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
       +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">사업자등록번호</label>'
       +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
       +'                	<i class="fa"></i>'
	    +'					<input type="text" id="bizRegNo" name="bizRegNo" class="form-control col-md-7 col-xs-12" maxlength="12" isBzno="true">'
	    +'					<span class="input-group-btn">'
       +'                    	<button class="btn btn-default btn-search bzno" type="button">중복</button>'
       +'                    </span>'
       +'                </div>'
       +'            </div>'
       +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
       +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">법인등록번호</label>'
       +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
       +'                	<i class="fa"></i>'
	    +'					<input type="text" id="corpRegNo" name="corpRegNo" class="form-control col-md-7 col-xs-12" maxlength="13">'
	    +'					<span class="input-group-btn">'
       +'                    	<button class="btn btn-default btn-search corpNo" type="button">중복</button>'
       +'                    </span>										'
       +'                </div>'
       +'            </div>'
       +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
       +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">업종</label>'
       +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
       +'                	<i class="fa"></i>'
	    +'					<input type="text" id="bizKind" name="bizKind" class="form-control col-lg-12 col-md-7 col-xs-12">'
       +'                </div>'
       +'            </div>'
       +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
       +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">업태</label>'
       +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
       +'                	<i class="fa"></i>'
	    +'					<input type="text" id="bizCond" name="bizCond" class="form-control col-lg-12 col-md-7 col-xs-12">'
       +'                </div>'
       +'            </div>'
       +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
       +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">우편번호</label>'
       +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
       +'                	<i class="fa"></i>'
	    +'					<input type="text" id="zipcode" name="zipcode" class="form-control col-md-7 col-xs-12">'
       +'                </div>'
       +'            </div>'
       +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
       +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">주소</label>'
       +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 input-icon left">'
       +'                	<i class="fa"></i>'
	    +'					<input type="text" id="address" name="address" class="form-control col-lg-12 col-md-7 col-xs-12">'
       +'                </div>'
       +'            </div>'
       +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
       +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">상세주소</label>'
       +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 input-icon left">'
	    +'					<i class="fa"></i>'
	    +'					<input type="text" id="addressDtl" name="addressDtl" class="form-control col-lg-12 col-md-7 col-xs-12">'
       +'                </div>'
       +'            </div>'
       +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
       +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">거래처구분</label>'
       +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">'
       +'                    <select class="form-control" id="bizGrp" name="bizGrp" >'
       +'                    </select>'
       +'                </div>'
       +'            </div>'
       +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
       +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표 연락처</label>'
       +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
       +'                	<i class="fa"></i>'
	    +'					<input type="text" id="tel" name="tel" class="form-control col-md-7 col-xs-12" isTel="true">'
       +'                </div>'
       +'            </div>'
       +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
       +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표 팩스번호</label>'
       +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">'
	    +'					<input type="text" id="fax" name="fax" class="form-control col-md-7 col-xs-12" isTel="true">'
       +'                </div>'
       +'            </div>'
	    +'		</div>'
       +'        <div class="col-md-12 col-sm-12 col-xs-12">'
       +'            <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
       +'                <label class="control-label col-md-3 col-sm-3 col-xs-12"><b>[세금계산서 정보]</b></label>'
       +'            </div>'
       +'        </div>'
	    +'		<div class="col-md-12 col-sm-12 col-xs-12">'
       +'            <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
       +'                <label class="control-label custom-col-lg-1 col-md-12 col-sm-12 col-xs-12">사용여부</label>'
       +'                <div class="custom-col-lg-10 col-md-12 col-sm-12 col-xs-12 form-inline">'
       +'                    <select class="form-control" id="useFlag" name="useFlag" >'
       +'                    	<option value="Y">사용</option>'
       +'                    	<option value="N">미사용</option>'
       +'                    </select>'
       +'                </div>'
       +'            </div>'
	    +'		</div>'
       +'    </form>'
       +'</div><br />';    	
}            


function setUpdDataFormat(merchantData){
	kpcUtil.setDatePicker('#merchantUptForm #openDt');
	kpcUtil.setSelectBoxData({
		target : "#merchantUptForm #bizGrp", 
		apiUrl : "/api/systemMng/common/commonCodes",
		params : {type :'MER'},
		type   : "GET",
		option : {width : 150},	
		callBack : function (data,target,option){
			for(var idx in data.data){
				$(target).append($("<option></option>")
						.attr("value" , data.data[idx].code)
						.text(data.data[idx].codeName));
			}
			$(target).select2(option);
        	setMerchantFormValidate();
        	kpcUtil.setFormData("#merchantUptForm" , merchantData);
        	$("#merchantUptForm").valid();   
        	kpcUtil.setFormTextFieldFormat({
				target : "#merchantUptForm"
			});                    	
		}
	});            	
}

function setMerchantFormValidate(){
    $("#merchantUptForm").validate({
        errorElement:'span', //default input error message container
        errorClass:'help-block help-block-error', // default input error message class
        rules: {
        	name : {
                required : true,
            },
            nameEng : {
                required : true,
            },
            bizKind : {
                required : true,
            },
            bizCond : {
                required : true,
            },
            bizGrp : {	
                required : true,
            },
            bizRegNo : {
                required : true,
                minlength : 10,
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
            tel : {
                required : true,
            },
            telSub : {
                required : true,
            },
            capitalAmount : {
            	number : true,
            },
            empCount : {
            	number : true,
            },
            storeCount : {
            	number : true,
            },
            avgSaleMonth : {
            	number : true,
            },
            avgSaleYear : {
            	number : true,
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
            bizGrp : {	
                required : "가맹점 구분을 선택해주세요.",
            },
            bizRegNo : {
                required : "사업자 번호를 입력해주세요.",
                minlength : "정확한 사업자번호를 입력해주세요.",
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
            tel : {
                required : "비밀번호를 입력해주세요.",
            },
            telSub : {
                required : "대표 연락처를 입력해주세요.",
            },
            capitalAmount : {
            	number : "숫자만 입력해주세요.",
            },
            empCount : {
            	number : "숫자만 입력해주세요.",
            },
            storeCount : {
            	number : "숫자만 입력해주세요.",
            },
            avgSaleMonth : {
            	number : "숫자만 입력해주세요.",
            },
            avgSaleYear : {
            	number : "숫자만 입력해주세요.",
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

}            