function serviceInfo(jsonParam){
	
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
			bodyHtml = serviceDetailContent();   				   			
   			buttonHtml ='<button type="button" class="dt-button btn green btn-outline btnAppr">승인처리</button>'
	               +'<button type="button" class="dt-button btn green btn-outline btnReject">반려</button>';
	} else if(status == "ARST-0003" && reqEmpId == empId && typeCode == "APPR-0300"){
		buttonHtml ='<button type="button" class="dt-button btn green btn-outline btnUpt">수정</button>';
		bodyHtml = serviceUpdateContent();
	} else{
		bodyHtml = serviceDetailContent();
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
	                        url: "/api/approval/service/approvals/approval",
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
				
				if($("#serviceUptForm").valid() && kpcUtil.confirm("수정 후 재승인요청 하시겠습니까?") ){
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
		   						var jsonData = $("#serviceUptForm").serializeJsonObject();
		   						jsonData["apprEmpId"] = updApprEmpId;
		   						jsonData["menuId"] = menuId;
		   						jsonData["tmpSeq"] = tmpSeq;
		   						jsonData["seq"] = seq;
       		             		$.ajax({
           		         			url: "/api/approval/service/approvals/reject/reApproval",
           		         			data: JSON.stringify(jsonData),
           		         			type:'POST',
           		         			dataType : "json",
           		         			contentType  : "application/json",
       		         			}).done(function (data){
   		                    		if(kpcUtil.successHandlingToMsg("#serviceUptForm",data,true,"승인 요청 되었습니다.")){
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
                       url: "/api/approval/service/approvals/serviceTmp",
                       data: "tmpSeq=" + tmpSeq,
                       type:'GET',
                       dataType : "json",
            	}).done(function(resultData,sts,jqXhr){
            		if(resultData["apprStatus"] == "ARST-0003" && resultData["apprTypeCode"] == "APPR-0300" && reqEmpId == empId){
            			setServiceUpdDataFormat(resultData);
            		} else {
            			kpcUtil.setFormData("#serviceDetailForm" , resultData);
            		}
                }).fail(function(e){
        	    	kpcUtil.errorHandling(e);
      	        });			            			   
    	   }
       }]
	});            		        			
}		

function serviceDetailContent(){
	return'<form action="#" id="serviceDetailForm" class="form-bordered ">'
	+'    <div class="col-md-12 col-sm-12 col-xs-12">'
	+'        <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
	+'            <label class="control-label col-md-3 col-sm-3 col-xs-12">- 기본정보 </label>'
	+'        </div>'
	+'    </div>'
	+'    <div class="col-md-12 col-sm-12 col-xs-12">'
	+'        <div class="col-lg-12 col-md-12 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right">'
	+'            <label class="control-label custom-col-lg-1 col-md-12 col-sm-12 col-xs-12">거래처코드</label>'
	+'            <div class="custom-col-lg-10 col-md-3 col-sm-4 col-xs-12 form-border-left-lg">'
	+'                <span id="submerchantId"   class="span-vertical-middle col-md-7 col-xs-12" ></span>'
	+'            </div>'
	+'        </div>'
	+'        <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
	+'            <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">서비스 코드</label>'
	+'            <div class="col-lg-9 col-md-12 col-sm-9 col-xs-12 form-border-left-lg">'
	+'                <span id="serviceId"  class="span-vertical-middle col-md-7 col-xs-12" ></span>'
	+'            </div>'
	+'        </div>'
	+'        <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
	+'            <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">서비스명</label>'
	+'            <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
	+'                <span id="name"  class="span-vertical-middle col-md-7 col-xs-12" ></span>'
	+'            </div>'
	+'        </div>'
	+'        <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
	+'            <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">서비스 타입</label>'
	+'            <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg ">'
	+'                <span  id="serviceTypeNm"  class="span-vertical-middle col-md-7 col-xs-12" ></span>'
	+'            </div>'
	+'        </div>'
	+'        <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
	+'            <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">서비스 카테고리</label>'
	+'            <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
	+'                <span  id="categoryNm"  class="span-vertical-middle col-md-7 col-xs-12" ></span>'
	+'            </div>'
	+'        </div>'
	+'        <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
	+'            <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">연동 아이디</label>'
	+'            <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
	+'            	'
	+'				<span id="svcConnId"  class="span-vertical-middle col-md-7 col-xs-12" ></span>'
	+'            </div>'
	+'        </div>'
	+'        <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
	+'            <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">서비스 사용 여부</label>'
	+'            <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
	+'                <span  id="useFlagNm"  class="span-vertical-middle col-md-7 col-xs-12" ></span>'
	+'            </div>'
	+'        </div>'
	+'        <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
	+'            <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">서비스구분</label>'
	+'            <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">'
	+'                <span  id="saleDividerNm" class="span-vertical-middle col-md-7 col-xs-12" ></span>'
	+'            </div>'
	+'        </div>'
	+'    </div>'
	+'</form>';
}

function serviceUpdateContent(){
	return''
        +'<div class="form">'
        +'<form action="#" id="serviceUptForm" class="form-bordered ">'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
        +'        <label class="control-label col-md-3 col-sm-3 col-xs-12">- 서비스 정보 </label>'
        +'    </div>'
        +'</div>'
        +'<div class="col-md-12 col-sm-12 col-xs-12">'
        +'    <div class="col-lg-12 col-md-12 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right">'
        +'        <label class="control-label custom-col-lg-1 col-md-12 col-sm-12 col-xs-12">거래처코드</label>'
        +'        <div class="custom-col-lg-10 col-md-3 col-sm-4 col-xs-12 form-inline input-icon left">'
        +'            <i class="fa"></i>'
        +'            <input type="text" id="submerchantId" name="submerchantId" class="form-control col-lg-7" readonly="readonly" >'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">서비스 코드</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-9 col-xs-12 form-inline input-icon left">'
        +'            <i class="fa"></i>'
        +'            <input type="text" id="serviceId" name="serviceId" class="form-control col-lg-7" readonly="readonly">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">서비스명</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'            <i class="fa"></i>'
        +'            <input type="text" id="name" name="name" class="form-control">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">서비스 타입</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'            <i class="fa"></i>'
        +'            <select class="form-control" id="serviceType" name="serviceType" >'
        +'            </select>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">서비스 카테고리</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'            <i class="fa"></i>'
        +'            <select class="form-control" id="category" name="category" >'
        +'            </select>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">연동 아이디</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'        	<i class="fa"></i>'
	    +'			<input type="text" id="svcConnId" name="svcConnId" class="form-control col-md-7 col-xs-12">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">연동 비밀번호</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">'
        +'        	<i class="fa"></i>'
	    +'			<input type="password" id="svcConnPw" name="svcConnPw" class="form-control col-md-7 col-xs-12">'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">서비스 사용 여부</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">'
        +'            <select class="form-control" id="useFlag" name="useFlag" >'
        +'            	<option value="Y">사용</option>'
        +'            	<option value="N">미사용</option>'
        +'            </select>'
        +'        </div>'
        +'    </div>'
        +'    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
        +'        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">서비스구분</label>'
        +'        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">'
        +'            <select class="form-control" id="saleDivider" name="saleDivider" >'
        +'            </select>'
        +'        </div>'
        +'    </div>'
        +'</div>'
        +'</form>'
        +'</div><br />';                                                                                                               
}

function setServiceUpdDataFormat(serviceData){
	console.log(serviceData);
    $("#serviceUptForm #useFlag").select2({
        width: 110,
    });	
	kpcUtil.setSelectBoxData({
		target : [
		          "#serviceUptForm #serviceType", 
		          "#serviceUptForm #category", 
		          "#serviceUptForm #saleDivider", 
		], 
		apiUrl : "/api/systemMng/common/commonCodeList",
		params : {type : 'SVRT,SVR,SVC'},
		type   : "GET",
		option : {width : 150},	
		callBack : function (data,target,option){
			for(var idx in data){
				for(var idx2 in data[idx].resultList){
					var tag = data[idx].resultList[idx2].codeName;
					if($(target[idx]) == "SVC"){
						tag = "<span title='"+data[idx].resultList[idx2].descText+ "' onmouseover='tooltipAdd(this)'>"+data[idx].resultList[idx2].codeName +"</span>";
					}
					$(target[idx]).append($("<option></option>")
							.attr("value" , data[idx].resultList[idx2].code)
							.text(tag));						
				}
				if($(target[idx]) == "SVC"){
					$(target[idx]).select2({
						escapeMarkup: function (m) { return m;},
						width : 120,
					});       					
				}else {
					$(target[idx]).select2(option);
				}
				kpcUtil.setFormData("#serviceUptForm" , serviceData);
				setServiceFormValidate();
			}
		}
	});			
}

function setServiceFormValidate(){
    $("#serviceUptForm").validate({
        errorElement: 'span', //default input error message container
        errorClass: 'help-block help-block-error', // default input error message class
        rules: {
        	submerchantId : {
                required : true,
            },
            serviceId: {
                required : true,
            },
            name: {
            	required : true,
            },
            serviceType: {
                required : true,
            },
            category: {
                required : true,
            },
			svcConnId: {
                required : true,
            },
			svcConnPw: {
                required : true,
            },
            useFlag: {
                required : true,
            },
        },
        messages : {
        	submerchantId : {
                required : "잘못된 접근입니다.",
            },
            serviceId : {
            	required : "잘못된 접근입니다.",
            },
            name: {
                required : "서비스명을 입력해주세요..",
            },
            serviceType: {
                required : "서비스타입을 선택해주세요.",
            },
            category: {
                required : "서비스 카테고리를 선택해주세요.",
            },
			svcConnId: {
                required : "연동 아이디를 입력해주세요.",
            },
			svcConnPw: {
                required : "연동 비밀번호를 입력해주세요.",
            },
            useFlag: {
                required : "서비스사용여부를 선택해주세요.",
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
        	console.log(element);
           	$(element).closest('.form-group').addClass('has-error'); // set error class to the control group
        },
        success : function (label,element){
        	var icon = $(element).parent(".input-icon").children('i');
        	$(element).closest(".form-group").removeClass("has-error").addClass("has-success");
        	icon.removeClass('fa-warning').addClass("fa-check");
        },
    });

}
