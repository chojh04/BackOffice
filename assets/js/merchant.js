function reMerchantUpdate(merchantId,callback){
	var bodyHtml = ''
        +'<div class="form">                                                                                                                   '
        +'    <form action="#" id="merchantUptForm" class="form-bordered ">                                                                       '
        +'        <div class="col-md-12 col-sm-12 col-xs-12">                                                                                  '
        +'            <div class="col-md-12 col-sm-12 col-xs-12 form-group ">                                                                  '
        +'                <label class="control-label col-md-3 col-sm-3 col-xs-12">- 대표 거래처 등록 </label>                                 '
        +'            </div>                                                                                                                   '
        +'        </div>                                                                                                                       '
        +'        <div class="col-md-12 col-sm-12 col-xs-12">                                                                                  '
        +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                      '
        +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표 거래처 코드</label>                         '
        +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                     '
        +'               		<i class="fa"></i>                                                                                            '
        +'                    <input type="text" id="merchantId" name="merchantId" class="form-control col-md-3 col-xs-12" readonly="readonly">'
        +'                </div>                                                                                                               '
        +'            </div>                                                                                                                   '
        +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                    '
        +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표 거래처 명</label>                           '
        +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                     '
        +'               		<i class="fa"></i>                                                                                            '
	    +'					<input type="text" id="name" name="name" class="form-control col-md-7 col-xs-12">                                 '
        +'                </div>                                                                                                               '
        +'            </div>                                                                                                                   '
        +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                      '
        +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표 거래처 약칭</label>                         '
        +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                     '
        +'                    <input type="text" id="alias" name="alias" class="form-control col-md-7 col-xs-12">                              '
        +'                </div>                                                                                                               '
        +'            </div>                                                                                                                   '
        +'        </div>                                                                                                                       '
        +'        <div class="col-md-12 col-sm-12 col-xs-12">                                                                                  '
        +'            <div class="col-md-12 col-sm-12 col-xs-12 form-group ">                                                                  '
        +'                <label class="control-label col-md-3 col-sm-3 col-xs-12"><b>[세금계산서 정보]</b></label>                            '
        +'            </div>                                                                                                                   '
        +'        </div>                                                                                                                       '
        +'        <div class="col-md-12 col-sm-12 col-xs-12">                                                                                  '
        +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                      '
        +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표 성명</label>                                '
        +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                     '
        +'                	<i class="fa"></i>                                                                                                '
        +'                    <input type="text" id="ceoName" name="ceoName" class="form-control col-md-7 col-xs-12">                          '
        +'                </div>                                                                                                               '
        +'            </div>                                                                                                                   '
        +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                    '
        +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">개업일</label>                                   '
        +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                     '
        +'                    <input type="text" class="form-control input-date-picker" id="openDate" name="openDate" isDateField="true">                        '
        +'                </div>                                                                                                               '
        +'            </div>                                                                                                                   '
        +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                      '
        +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">사업자등록번호</label>                           '
        +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                     '
        +'                	<i class="fa"></i>                                                                                                '
	    +'					<input type="text" id="bizRegNo" name="bizRegNo" class="form-control col-md-7 col-xs-12" maxlength="12" isBzno="true">          '
	    +'					<span class="input-group-btn">                                                                                    '
        +'                    	<button class="btn btn-default btn-search bzno" type="button">중복</button>                                   '
        +'                    </span>                                                                                                          '
        +'                </div>                                                                                                               '
        +'            </div>                                                                                                                   '
        +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                    '
        +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">법인등록번호</label>                             '
        +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                     '
        +'                	<i class="fa"></i>                                                                                                '
	    +'					<input type="text" id="corpRegNo" name="corpRegNo" class="form-control col-md-7 col-xs-12" maxlength="13">        '
	    +'					<span class="input-group-btn">                                                                                    '
        +'                    	<button class="btn btn-default btn-search corpNo" type="button">중복</button>                                 '
        +'                    </span>										                                                                  '
        +'                </div>                                                                                                               '
        +'            </div>                                                                                                                   '
        +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                      '
        +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">업종</label>                                     '
        +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                     '
        +'                	<i class="fa"></i>                                                                                                '
	    +'					<input type="text" id="bizKind" name="bizKind" class="form-control col-lg-12 col-md-7 col-xs-12">                 '
        +'                </div>                                                                                                               '
        +'            </div>                                                                                                                   '
        +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                    '
        +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">업태</label>                                     '
        +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                     '
        +'                	<i class="fa"></i>                                                                                                '
	    +'					<input type="text" id="bizCond" name="bizCond" class="form-control col-lg-12 col-md-7 col-xs-12">                 '
        +'                </div>                                                                                                               '
        +'            </div>                                                                                                                   '
        +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                      '
        +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">우편번호</label>                                 '
        +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                     '
        +'                	<i class="fa"></i>                                                                                                '
	    +'					<input type="text" id="zipcode" name="zipcode" class="form-control col-md-7 col-xs-12">                           '
        +'                </div>                                                                                                               '
        +'            </div>                                                                                                                   '
        +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                    '
        +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">주소</label>                                     '
        +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 input-icon left">                                                 '
        +'                	<i class="fa"></i>                                                                                                '
	    +'					<input type="text" id="address" name="address" class="form-control col-lg-12 col-md-7 col-xs-12">                 '
        +'                </div>                                                                                                               '
        +'            </div>                                                                                                                   '
        +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                      '
        +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">상세주소</label>                                 '
        +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 input-icon left">                                                 '
	    +'					<i class="fa"></i>                                                                                                 '
	    +'					<input type="text" id="addressDetail" name="addressDetail" class="form-control col-lg-12 col-md-7 col-xs-12">      '
        +'                </div>                                                                                                               '
        +'            </div>                                                                                                                   '
        +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                    '
        +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">거래처구분</label>                               '
        +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                     '
        +'                    <select class="form-control" id="bizGrp" name="bizGrp" >                                                         '
        +'                    </select>                                                                                                        '
        +'                </div>                                                                                                               '
        +'            </div>                                                                                                                   '
        +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                      '
        +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표 연락처</label>                              '
        +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                     '
        +'                	<i class="fa"></i>                                                                                                '
	    +'					<input type="text" id="tel" name="tel" class="form-control col-md-7 col-xs-12" isTel="true">                                   '
        +'                </div>                                                                                                               '
        +'            </div>                                                                                                                   '
        +'            <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                    '
        +'                <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표 팩스번호</label>                            '
        +'                <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                     '
	    +'					<input type="text" id="fax" name="fax" class="form-control col-md-7 col-xs-12" isTel="true">                                   '
        +'                </div>                                                                                                               '
        +'            </div>                                                                                                                   '
	    +'		</div>                                                                                                                        '
        +'        <div class="col-md-12 col-sm-12 col-xs-12">                                                                                  '
        +'            <div class="col-md-12 col-sm-12 col-xs-12 form-group ">                                                                  '
        +'                <label class="control-label col-md-3 col-sm-3 col-xs-12"><b>[세금계산서 정보]</b></label>                            '
        +'            </div>                                                                                                                   '
        +'        </div>                                                                                                                       '
	    +'		<div class="col-md-12 col-sm-12 col-xs-12">                                                                                   '
        +'            <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                     '
        +'                <label class="control-label custom-col-lg-1 col-md-12 col-sm-12 col-xs-12">사용여부</label>                          '
        +'                <div class="custom-col-lg-10 col-md-12 col-sm-12 col-xs-12 form-inline">                                             '
        +'                    <select class="form-control" id="useFlag" name="useFlag" >                                                       '
        +'                    	<option value="Y">사용</option>                                                                               '
        +'                    	<option value="N">미사용</option>                                                                             '
        +'                    </select>                                                                                                        '
        +'                </div>                                                                                                               '
        +'            </div>                                                                                                                   '
	    +'		</div>                                                                                                                        '
        +'    </form>                                                                                                                          '
        +'</div><br />                                                                                                                             ';                            
	var buttonHtml = '<button type="button" class="dt-button btn green btn-outline btnSave">수정</button>';
	kpcUtil.openCommonPopup({
		modalTitle : "대표 거래처 수정",
		bodyHtml : bodyHtml,
		button : buttonHtml,
		modalSize : "modal-full",
		buttonEvent : [
			// 대표 거래처 수정 이벤트
   			{
   				target : ".btnSave",
   				eventType : "click",
   				callBack : function (){
   					if(kpcUtil.bzNoDupCheck("#merchantUptForm #bizRegNo", "#merchantUptForm")){
   						return false;
   					}
   					if($("#merchantUptForm").valid() && kpcUtil.confirm("승인 신청 하시겠습니까?") ){

                    	var menuId = "MCM-0002";
                    	// 승인자 선택
                    	kpcPopupUtil.openApprListPop({
                    		 menuId : menuId 
                    		,callBack : function (data){
                    			var apprEmpId = $("input[name=empList]:checked").attr("empId");
                    			console.log(apprEmpId);
   			   					if(typeof apprEmpId === "undefined"){
   			   						kpcUtil.customAlert("승인자를 선택해주세요.");
   			   						return false;
   			   					} else {
   			   						var jsonData = $("#merchantUptForm").serializeJsonObject();
   			   						jsonData["apprEmpId"] = apprEmpId;
   			   						jsonData["menuId"] = menuId;
       			                    $.ajax({
       		                           url: "/api/merchants/merchant/represent",
       		                           data: JSON.stringify(jsonData),
       		                           type: 'PUT',
       		                           dataType : "json",
       		                           contentType  : "application/json",
       		                    	}).done(function(resultData,status,jqXhr){
       		                    		if(kpcUtil.successHandling("#merchantUptForm",resultData,true)){
       		                    			$(".modal").modal('toggle');
       		                    		}
       		                        }).fail(function(e){
       		                	    	kpcUtil.errorHandling(e);
       		               	        });
   			   					}
                    		}
                    	});      						
   					}
   				}
   			},
   			// 사업자번호 중복체크
   			{
   				target : ".bzno",
   				eventType : "click",
   				callBack : function (){
   					kpcUtil.bzNoCheck("#merchantUptForm #bizRegNo", "#merchantUptForm");
   				}
   			},
   			// 법인번호 중복체크
   			{
   				target : ".corpNo",
   				eventType : "click",
   				callBack : function (){
   					kpcUtil.corpNoCheck("#merchantUptForm #corpRegNo", "#merchantUptForm");
   				}
   			},
   			// 모달 이벤트
   			{
   				target : ".modal",
   				eventType : "shown.bs.modal",
   				callBack : function (){
					setDatePicker();
					setCommonCode(merchantId);
					setFormValidate();
					kpcUtil.setFormTextFieldFormat({
						target : "#merchantUptForm"
					});

   				}
   			}       			
		]
	});
}

function getMerchant(merchantId){
	$.ajax({
        url: "/api/merchants/merchant/represent",
        data : "merchantId=" + merchantId,
        type: 'GET',
        dataType : "json",
        contentType  : "application/json",
        async : true,
        success: function(data){
        	kpcUtil.setFormData("#merchantUptForm" , data)
        	$("#merchantUptForm").valid();
        },
        error : function(e){
        	kpcUtil.errorHandling(e);
        }
    });	
}

function setCommonCode(merchantId){
	kpcUtil.setSelectBoxData({
		target : "#merchantUptForm #bizGrp", 
		apiUrl : "/api/systemMng/common/commonCodes",
		params : {type : 'MER'},
		type   : "GET",
		option : {width : 150},	
		callBack : function (data,target,option){
			for(var idx in data.data){
				$(target).append($("<option></option>")
						.attr("value" , data.data[idx].code)
						.text(data.data[idx].codeName));
			}
			$(target).select2(option);
			getMerchant(merchantId);
		}
	});

}

function setDatePicker(){
    kpcUtil.setDatePicker('#merchantUptForm #openDate');
}            

function setFormValidate(){
    $("#merchantUptForm").validate({
        errorElement: 'span', //default input error message container
        errorClass: 'help-block help-block-error', // default input error message class
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


function subMerchantUpdate(merchantId,callback){
	var bodyHtml = ''
        + '<div class="form">                                                                                                                   '
        + '<form action="#" id="merchantUptForm" class="form-bordered ">'
        + '<input type="hidden" id="parentId" name="parentId" >                                                                                '
        + '<input type="hidden" id="encAgentPw" name="encAgentPw" >                                                                                '
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                         '
        + '    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">                                                                         '
        + '        <label class="control-label col-md-3 col-sm-3 col-xs-12">- 거래처 정보 </label>                                             '
        + '    </div>                                                                                                                          '
        + '</div>                                                                                                                              '
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                         '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                             '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">거래처 코드</label>                                     '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                            '
        + '       		<i class="fa"></i>                                                                                                   '
        + '            <input type="text" id="submerchantId" name="submerchantId" class="form-control col-md-3 col-xs-12" readonly="readonly"> '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                           '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">거래처 명</label>                                       '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                            '
        + '       		<i class="fa"></i>                                                                                                   '
        + '			<input type="text" id="name" name="name" class="form-control col-md-7 col-xs-12 lang-ko"  >                              '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                             '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">거래처약칭</label>                                      '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                            '
        + '       		<i class="fa"></i>                                                                                                   '
        + '			<input type="text" id="alias" name="alias" class="form-control col-md-7 col-xs-12">                                      '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '</div>                                                                                                                              '
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                         '
        + '    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">                                                                         '
        + '        <label class="control-label col-md-3 col-sm-3 col-xs-12">                                                                   '
        + '        	<span>                                                                                                                   '
        + '        		<b>[세금계산서 정보]</b>                                                                                             '
        + '        	</span>                                                                                                                  '
        + '        </label>                                                                                                                    '
        + '    </div>                                                                                                                          '
        + '</div>                                                                                                                              '
        + '<div class="col-md-12 col-sm-12 col-xs-12" id="taxDiv">                                                                             '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                             '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표 성명</label>                                       '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                            '
        + '        	<i class="fa"></i>                                                                                                       '
        + '            <input type="text" id="ceoName" name="ceoName" class="form-control col-md-7 col-xs-12">                                 '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                           '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">개업일</label>                                          '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                            '
        + '            <input type="text" class="form-control input-date-picker" id="openDate" name="openDate" isDateField="true">             '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                             '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">사업자등록번호</label>                                  '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                            '
        + '        	<i class="fa"></i>                                                                                                       '
        + '			<input type="text" id="bizRegNo" name="bizRegNo" class="form-control col-md-7 col-xs-12" maxlength="12" isBzno="true">                 '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                           '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">법인등록번호</label>                                    '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                            '
        + '        	<i class="fa"></i>                                                                                                       '
        + '			<input type="text" id="corpRegNo" name="corpRegNo" class="form-control col-md-7 col-xs-12" maxlength="13">               '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                             '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">업종</label>                                            '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                            '
        + '        	<i class="fa"></i>                                                                                                       '
        + '			<input type="text" id="bizKind" name="bizKind" class="form-control col-lg-12 col-md-7 col-xs-12">                        '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                           '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">업태</label>                                            '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                            '
        + '        	<i class="fa"></i>                                                                                                       '
        + '			<input type="text" id="bizCond" name="bizCond" class="form-control col-lg-12 col-md-7 col-xs-12">                        '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                             '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">우편번호</label>                                        '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                            '
        + '        	<i class="fa"></i>                                                                                                       '
        + '			<input type="text" id="zipcode" name="zipcode" class="form-control col-md-7 col-xs-12">                                  '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                           '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">주소</label>                                            '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 input-icon left">                                                        '
        + '        	<i class="fa"></i>                                                                                                       '
        + '			<input type="text" id="address" name="address" class="form-control col-lg-12 col-md-7 col-xs-12">                        '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                             '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12 ">상세주소</label>                                       '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 input-icon left">                                                        '
        + '        	<i class="fa"></i>                                                                                                       '
        + '			<input type="text" id="addressDetail" name="addressDetail" class="form-control col-lg-12 col-md-7 col-xs-12">              '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                           '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">거래처구분</label>                                      '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                            '
        + '            <select class="form-control" id="bizGrp" name="bizGrp" >                                                                '
        + '            </select>                                                                                                               '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                             '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표 연락처</label>                                     '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline ">                                                           '
        + '			<input type="text" id="tel" name="tel" class="form-control col-md-7 col-xs-12" isTel="true">                                          '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                           '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">대표 팩스번호</label>                                   '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                            '
        + '			<input type="text" id="fax" name="fax" class="form-control col-md-7 col-xs-12" isTel="true">                                          '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '</div>                                                                                                                              '
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                         '
        + '    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">                                                                         '
        + '        <label class="control-label col-md-3 col-sm-3 col-xs-12"><b>[전자세금계산서 발행정보]</b></label>                           '
        + '    </div>                                                                                                                          '
        + '</div>                                                                                                                              '
        + '<div class="col-md-12 col-sm-12 col-xs-12" >                                                                                        '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                             '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">세금계산서 담당자</label>                               '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                            '
        + '        	<i class="fa"></i>                                                                                                       '
        + '			<input type="text" id="taxCustNm" name="taxCustNm" class="form-control col-md-7 col-xs-12">                              '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                           '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">전화번호</label>                                        '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                            '
        + '			<input type="text" id="taxTel" name="taxTel" class="form-control col-md-7 col-xs-12" isTel="true">                                    '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                             '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">팩스번호</label>                                        '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                            '
        + '			<input type="text" id="taxFax" name="taxFax" class="form-control col-md-7 col-xs-12" isTel="true">                                    '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                           '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">핸드폰번호</label>                                      '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                            '
        + '			<input type="text" id="taxPhone" name="taxPhone" class="form-control col-md-7 col-xs-12" isTel="true">                                '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                             '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">E-MAIL</label>                                          '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                            '
        + '        	<i class="fa"></i>                                                                                                       '
        + '			<input type="text" id="taxEmail" name="taxEmail" class="form-control col-lg-12 col-lg-7 col-xs-12">                      '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '</div>                                                                                                                              '
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                         '
        + '    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">                                                                         '
        + '        <label class="control-label col-md-3 col-sm-3 col-xs-12"><b>[계좌정보]</b></label>                                          '
        + '    </div>                                                                                                                          '
        + '</div>                                                                                                                              '
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                         '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                             '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">은행</label>                                            '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                            '
        + '        	<i class="fa"></i>                                                                                                         '
		+ '             <select class="form-control isSelectValid" id="bankCd" name="bankCd">                                                  '
		+ '                 <option value="">선택</option>                                                                                     '
        + '             </select>                                                                                                              '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                           '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12 input-icon left">계좌번호</label>                        '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                            '
        + '        	<i class="fa"></i>                                                                                                         '
        + '			<input type="text" id="bankAccNo" name="bankAccNo" class="form-control col-md-7 col-xs-12">                                '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                             '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">예금주</label>                                          '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                            '
        + '        	<i class="fa"></i>                                                                                                         '
        + '			<input type="text" id="bankHolder" name="bankHolder" class="form-control col-md-7 col-xs-12">                              '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '</div>                                                                                                                              '
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                         '
        + '    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">                                                                         '
        + '        <label class="control-label col-md-3 col-sm-3 col-xs-12"><b>[거래처 담당자정보]</b></label>                                 '
        + '    </div>                                                                                                                          '
        + '</div>                                                                                                                              '
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                         '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                             '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">영업담당자</label>                                      '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline ">                                                           '
        + '			<input type="text" id="salesNm" name="salesNm" class="form-control col-md-7 col-xs-12">                                  '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                           '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">영업담당자 연락처</label>                               '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                            '
        + '			<input type="text" id="salesTel" name="salesTel" class="form-control col-md-7 col-xs-12" isTel="true">                                '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                             '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자</label>                                      '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline ">                                                           '
        + '			<input type="text" id="billingNm" name="billingNm" class="form-control col-md-7 col-xs-12">                              '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                           '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자 연락처</label>                               '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                            '
        + '			<input type="text" id="billingTel" name="billingTel" class="form-control col-md-7 col-xs-12" isTel="true">                            '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '</div>                                                                                                                              '
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                         '
        + '    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">                                                                         '
        + '        <label class="control-label col-md-3 col-sm-3 col-xs-12">[KPC 담당자정보]</label>                                           '
        + '    </div>                                                                                                                          '
        + '</div>                                                                                                                              '
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                         '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                             '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">영업담당자</label>                                      '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline ">                                                           '
        + '			<input type="text" id="kpcSalesNm" name="kpcSalesNm" class="form-control col-md-7 col-xs-12">                            '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                           '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">영업담당자 연락처</label>                               '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                            '
        + '			<input type="text" id="kpcSalesTel" name="kpcSalesTel" class="form-control col-md-7 col-xs-12" isTel="true">                          '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                             '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자</label>                                      '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline ">                                                           '
        + '			<input type="text" id="kpcBillingNm" name="kpcBillingNm" class="form-control col-md-7 col-xs-12">                           '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                           '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자 연락처</label>                               '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                            '
        + '			<input type="text" id="kpcBillingTel" name="kpcBillingTel" class="form-control col-md-7 col-xs-12" isTel="true">                         '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '</div>                                                                                                                              '
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                         '
        + '    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">                                                                         '
        + '        <label class="control-label col-md-3 col-sm-3 col-xs-12"><b>[연동정보]</b></label>                                          '
        + '    </div>                                                                                                                          '
        + '</div>                                                                                                                              '
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                         '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                             '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">에이전트 아이디</label>                                 '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                            '
        + '        	<i class="fa"></i>                                                                                                       '
        + '			<input type="text" id="agentId" name="agentId" class="form-control col-md-7 col-xs-12">                                  '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                           '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">에이전트 비밀번호</label>                               '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                            '
        + '        	<i class="fa"></i>                                                                                                       '
        + '			<input type="password" id="agentPw" name="agentPw" class="form-control col-md-7 col-xs-12">                              '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '</div>                                                                                                                              '
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                         '
        + '    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">                                                                         '
        + '        <label class="control-label col-md-3 col-sm-3 col-xs-12"><b>[기타정보]</b></label>                                          '
        + '    </div>                                                                                                                          '
        + '</div>                                                                                                                              '
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                         '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                             '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">사용여부</label>                                        '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                            '
        + '            <select class="form-control" id="useFlag" name="useFlag" >                                                              '
        + '            	<option value="Y">사용</option>                                                                                      '
        + '            	<option value="N">미사용</option>                                                                                    '
        + '            </select>                                                                                                               '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                           '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">홈페이지 URL</label>                                    '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                            '
        + '			<input type="text" id="urlHome" name="urlHome" class="form-control col-lg-12 col-md-12 col-xs-12">                       '
        + '        </div>                                                                                                                      '
        + '    </div>                                                                                                                          '
        + '</div>                                                                                                                              '        
        + '</form>                                                                                                                          '
        + '</div><br />                                                                                                                             ';                            
	var buttonHtml = '<button type="button" class="dt-button btn green btn-outline btnSave">수정</button>';
	kpcUtil.openCommonPopup({
		modalTitle : "일반 거래처 수정",
		bodyHtml : bodyHtml,
		button : buttonHtml,
		modalSize : "modal-full",
		buttonEvent : [
			// 대표 거래처 수정 이벤트
   			{
   				target : ".btnSave",
   				eventType : "click",
   				callBack : function (){
   					if($("#merchantUptForm").valid() && kpcUtil.confirm("승인 신청 하시겠습니까?") ){

   						var menuId = "MCM-0003";
                    	// 승인자 선택
                    	kpcPopupUtil.openApprListPop({
                    		 menuId : menuId 
                    		,callBack : function (data){
                    			var apprEmpId = $("input[name=empList]:checked").attr("empId");
   			   					if(typeof apprEmpId === "undefined"){
   			   						kpcUtil.customAlert("승인자를 선택해주세요.");
   			   						return false;
   			   					} else {
   			   						var jsonData = $("#merchantUptForm").serializeJsonObject();
   			   						jsonData["apprEmpId"] = apprEmpId;
   			   						jsonData["menuId"] = menuId;
       			                    $.ajax({
       		                           url: "/api/merchants/merchant",
       		                           data: JSON.stringify(jsonData),
       		                           type: 'PUT',
       		                           dataType : "json",
       		                           contentType  : "application/json",
       		                    	}).done(function(resultData,status,jqXhr){
       		                    		if(kpcUtil.successHandling("#merchantUptForm",resultData,true)){
       		                    			$(".modal").modal('toggle');
       		                    		}
       		                        }).fail(function(e){
       		                	    	kpcUtil.errorHandling(e);
       		               	        });
   			   					}
                    		}
                    	});      						

   					}
   				}
   			},
   			// 모달 이벤트
   			{
   				target : ".modal",
   				eventType : "shown.bs.modal",
   				callBack : function (){
   					setSubSelect2();
   					setDatePicker();
   					setSubCommonCode(merchantId);
					setSubFormValidate();
					kpcUtil.setFormTextFieldFormat({
						target : "#merchantUptForm"
					});					
   					$(".taxLoad").click(function (){
   						var bodyHtml = '<div class="row" style="margin-top:10px;">'
   				            + '<div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 form-group">'
   				            + '         <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 md-radio-inline">'
   				            + '         	<div class="md-radio">'
   				            + '         		<input type="radio" id="loadFlag1" name="loadFlag" value="Y" checked="checked">' 
   				            + '         		<label for="loadFlag1">'
   				            + '         			<span></span>'
   				            + '         			<span class="check"></span>'
   				            + '         			<span class="box"></span>'
   				            + '	대표거래처정보'
   				            + '         		</label>'
   				            + '         	</div>'
   				            + '         	<div class="md-radio">'
   				            + '         		<input type="radio" id="loadFlag2" name="loadFlag" value="N">'
   				            + '         		<label for="loadFlag2">'
   				            + '         			<span></span>'
   				            + '         			<span class="check"></span>'
   				            + '         			<span class="box"></span>'
   				            + '새로작성'
   				            + '         		</label>'
   				            + '         	</div>'
   				        	+ '         </div>'
   				               + '</div>'
   				               + '</div>'
   				            ;
   				   		var buttonHtml = '<button type="button" class="dt-button btn green btn-outline btnSave">확인</button>';
   				   		kpcUtil.openCommonPopup({
   				   			modalTitle : "불러오기",
   				   			bodyHtml : bodyHtml,
   				   			button : buttonHtml,
   				   			modalSize : "modal-sm",
   				   			buttonEvent : [{
   				   				target : ".btnSave",
   				   				eventType : "click",
   				   				callBack : function (){
   				   					if($("input[name=loadFlag]:checked").val() == "Y"){
				                        $.ajax({
   					                        url: "/api/merchants/merchant",
   					                        data: "merchantId=" + $("#merchantUptForm #parentId").val(),
   					                        type: 'GET',
   					                        dataType : "json",
   					                        contentType  : "application/json",
   				   						}).done(function(data){
   				   							kpcUtil.setFormData("#taxDiv" , data);
   				   							kpcUtil.setFormReadonly("#taxDiv",true);
   				   							$("#taxCustNm").focus();
   				   						}).fail(function (e){
   				                              	kpcUtil.errorHandling(e);
   				   						}); 
   				   					}else{
   				   						kpcUtil.setFormReadonly("#taxDiv",false);
   				   						kpcUtil.resetDiv("#taxDiv");
   				   						$("#ceoName").focus();
   				   					}
   										$(".modal").modal('toggle');
   				   				}
   				   			}]
   				   		});            		
   						
   					});   					
   				}
   			}       			
		]
	});
}


var setSubSelect2 = function () {
    $("#merchantUptForm #useFlag").select2({
        width: 110,
    }); 
}            

var getSubMerchant = function (merchantId){
	$.ajax({
        url: "/api/merchants/merchant",
        data : "merchantId=" + merchantId,
        type: 'GET',
        dataType : "json",
        contentType  : "application/json",
        async : true,
        success: function(data){
        	kpcUtil.setFormData("#merchantUptForm" , data)
			$("#encAgentPw").val($("#agentPw").val());
        	$("#merchantUptForm").valid();
        },
        error : function(e){
        	kpcUtil.errorHandling(e);
        }
    });	
}

var setSubCommonCode = function (merchantId){
	
		kpcUtil.setSelectBoxData({
		target : [
		          "#merchantUptForm #bizGrp",
		          "#merchantUptForm #bankCd",
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
			getSubMerchant(merchantId);
		}
	});

}            


var setSubFormValidate = function (){
    $("#merchantUptForm").validate({
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
            bizGrp : {	
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
            bizGrp : {	
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
	$("#merchantUptForm .isSelectValid").on("change" , function (){
		$(this).valid();
	});	        

}


function serviceUpdate(serviceId,callback){
	var bodyHtml = ''
        + '<div class="form">'
        + '<form action="#" id="serviceUptForm" class="form-bordered ">'
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                  '
        + '    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">                                                                  '
        + '        <label class="control-label col-md-3 col-sm-3 col-xs-12">- 서비스 정보 </label>                                      '
        + '    </div>                                                                                                                   '
        + '</div>                                                                                                                       '
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                  '
        + '    <div class="col-lg-12 col-md-12 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right">            '
        + '        <label class="control-label custom-col-lg-1 col-md-12 col-sm-12 col-xs-12">거래처코드</label>                        '
        + '        <div class="custom-col-lg-10 col-md-3 col-sm-4 col-xs-12 form-inline input-icon left">                               '
        + '            <i class="fa"></i>                                                                                               '
        + '            <input type="text" id="submerchantId" name="submerchantId" class="form-control col-lg-7" readonly="readonly" >   '
        + '        </div>                                                                                                               '
        + '    </div>                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                      '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">서비스 코드</label>                              '
        + '        <div class="col-lg-9 col-md-12 col-sm-9 col-xs-12 form-inline input-icon left">                                      '
        + '            <i class="fa"></i>                                                                                               '
        + '            <input type="text" id="serviceId" name="serviceId" class="form-control col-lg-7" readonly="readonly">            '
        + '        </div>                                                                                                               '
        + '    </div>                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                    '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">서비스명</label>                                 '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                     '
        + '            <i class="fa"></i>                                                                                               '
        + '            <input type="text" id="name" name="name" class="form-control">                                                   '
        + '        </div>                                                                                                               '
        + '    </div>                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                      '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">서비스 타입</label>                              '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline ">                                                    '
        + '            <select class="form-control" id="serviceType" name="serviceType" >                                               '
        + '            </select>                                                                                                        '
        + '        </div>                                                                                                               '
        + '    </div>                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                    '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">서비스 카테고리</label>                          '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                     '
        + '            <select class="form-control" id="category" name="category" >                                                     '
        + '            </select>                                                                                                        '
        + '        </div>                                                                                                               '
        + '    </div>                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                      '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">연동 아이디</label>                              '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                     '
        + '        	<i class="fa"></i>                                                                                                  '
	    + '			<input type="text" id="svcConnId" name="svcConnId" class="form-control col-md-7 col-xs-12">                         '
        + '        </div>                                                                                                               '
        + '    </div>                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                    '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">연동 비밀번호</label>                            '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                     '
        + '        	<i class="fa"></i>                                                                                                  '
	    + '			<input type="password" id="svcConnPw" name="svcConnPw" class="form-control col-md-7 col-xs-12">                     '
        + '        </div>                                                                                                               '
        + '    </div>                                                                                                                   '
        + '    <!-- <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                 '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">에이전트 아이디</label>                          '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                     '
        + '        	<i class="fa"></i>                                                                                                  '
	    + '			<input type="text" id="agentId" name="agentId" class="form-control col-md-7 col-xs-12">                             '
        + '        </div>                                                                                                               '
        + '    </div>                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                    '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">에이전트 비밀번호</label>                        '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                     '
        + '        	<i class="fa"></i>                                                                                                  '
	    + '			<input type="password" id="agentPw" name="agentPw" class="form-control col-md-7 col-xs-12">                         '
        + '        </div>                                                                                                               '
        + '    </div> -->                                                                                                               '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                      '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">서비스 사용 여부</label>                         '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                     '
        + '            <select class="form-control" id="useFlag" name="useFlag" >                                                       '
        + '            	<option value="Y">사용</option>                                                                                 '
        + '            	<option value="N">미사용</option>                                                                               '
        + '            </select>                                                                                                        '
        + '        </div>                                                                                                               '
        + '    </div>                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                    '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">서비스구분</label>                             '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                     '
        + '            <select class="form-control" id="saleDivider" name="saleDivider" >                            '
        + '            </select>                                                                                                        '
        + '        </div>                                                                                                               '
        + '    </div>                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                      '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">거래처경로</label>                               '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-border-left-lg">                                             '
        + '            <span id="path" class=" col-md-12 col-xs-12 span-vertical-middle"></span>                                        '
        + '        </div>                                                                                                               '
        + '    </div>                                                                                                                   '
        + '</div>                                                                                                                       '
        + '</form>'
        + '</div><br />';                                                                                                               
	var buttonHtml = '<button type="button" class="dt-button btn green btn-outline btnSave">수정</button>';
	kpcUtil.openCommonPopup({
		modalTitle : "서비스 수정",
		bodyHtml : bodyHtml,
		button : buttonHtml,
		modalSize : "modal-full",
		buttonEvent : [
			// 대표 거래처 수정 이벤트
   			{
   				target : ".btnSave",
   				eventType : "click",
   				callBack : function (){
   					if($("#serviceUptForm").valid() && kpcUtil.confirm("승인 신청 하시겠습니까?") ){
                    	var menuId = "MCM-0003";
                    	// 승인자 선택
                    	kpcPopupUtil.openApprListPop({
                    		 menuId : menuId 
                    		,callBack : function (data){
                    			var apprEmpId = $("input[name=empList]:checked").attr("empId");
                    			console.log(apprEmpId);
   			   					if(typeof apprEmpId === "undefined"){
   			   						kpcUtil.customAlert("승인자를 선택해주세요.");
   			   						return false;
   			   					} else {
   			   						var jsonData = $("#serviceUptForm").serializeJsonObject();
   			   						jsonData["apprEmpId"] = apprEmpId;
   			   						jsonData["menuId"] = menuId;
       			                    $.ajax({
       		                           url: "/api/merchants/services/service",
       		                           data: JSON.stringify(jsonData),
       		                           type: 'PUT',
       		                           dataType : "json",
       		                           contentType  : "application/json",
       		                    	}).done(function(resultData,status,jqXhr){
       		                    		if(kpcUtil.successHandling("#serviceUptForm",resultData,true)){
       		                    			$(".modal").modal('toggle');
       		                    		}
       		                        }).fail(function(e){
       		                	    	kpcUtil.errorHandling(e);
       		               	        });
   			   					}
                    		}
                    	});      						
   					}
   				}
   			},
   			// 모달 이벤트
   			{
   				target : ".modal",
   				eventType : "shown.bs.modal",
   				callBack : function (){
   					setServiceFormValidate();
   					setServiceSelect2();
   					setServiceCommonCode(serviceId);
   				}
   			}       			
		]
	});
}

function getServiceData(serviceId){
	$.ajax({
        url: "/api/merchants/services/service",
        data : "serviceId=" + serviceId,
        type: 'GET',
        dataType : "json",
        contentType  : "application/json",
	}).done(function(data){
    	kpcUtil.setFormData("#serviceUptForm" , data)
    	$("#serviceUptForm").valid();
    }).fail(function(e){
        	kpcUtil.errorHandling(e);
    });	
}


function setServiceSelect2 () {
    $("#serviceUptForm #useFlag").select2({
        width: 110,
    });

}          
function setServiceCommonCode(serviceId){
	kpcUtil.setSelectBoxData({
		target : [
		          "#serviceUptForm #serviceType", 
		          "#serviceUptForm #category", 
		], 
		apiUrl : "/api/systemMng/common/commonCodeList",
		params : {type : 'SVRT,SVRT'},
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
				getServiceData(serviceId);
			}
		}
	});			
	kpcUtil.setSelectBoxData({
			target : [
			          "#serviceUptForm #saleDivider", 
			], 
			apiUrl : "/api/systemMng/common/commonCodeList",
			params : {type : 'SVC'},
			type   : "GET",
			option : {
						width : 150,
			},	
			callBack : function (data,target,option){
				for(var idx in data){
					for(var idx2 in data[idx].resultList){
						var tag = "<span title='"+data[idx].resultList[idx2].descText+ "' onmouseover='tooltipAdd(this)'>"+data[idx].resultList[idx2].codeName +"</span>";
	    				$(target[idx]).append($("<option></option>")
	    						.attr("value" , data[idx].resultList[idx2].code)
	    						.text(tag));
					}
					$(target[idx]).select2({
						escapeMarkup: function (m) { return m;},
						width : 120,
					});       
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
			agentId: {
                required : true,
            },
			agentPw: {
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
			agentId: {
                required : "에이전트 아이디를 입력해주세요.",
            },
			agentPw: {
                required : "에이전트 비밀번호를 입력해주세요",
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
           	$(element).closest('.form-group').addClass('has-error'); // set error class to the control group
        },
        success : function (label,element){
        	var icon = $(element).parent(".input-icon").children('i');
        	$(element).closest(".form-group").removeClass("has-error").addClass("has-success");
        	icon.removeClass('fa-warning').addClass("fa-check");
        },
    });

}

function billingUpdate(serviceBillingId,callback){
	var bodyHtml = ''
        + '<div class="form">'                                                                                                                          
        + '<form action="#" id="billingUptForm" class="form-bordered ">'                                                                                
        + '<input type="hidden" id="serviceId" name="serviceId">'
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                                  '
        + '    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">                                                                                  '
        + '        <label class="control-label col-md-3 col-sm-3 col-xs-12">- 정산정보 </label>                                                         '
        + '    </div>                                                                                                                                   '
        + '</div>                                                                                                                                       '
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                                  '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                                      '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산코드</label>                                                 '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                                     '
        + '       		<i class="fa"></i>                                                                                                              '
        + '            <input type="text" id="serviceBillingId" name="serviceBillingId" class="form-control col-md-3 col-xs-12" readonly="readonly">    '
        + '        </div>                                                                                                                               '
        + '    </div>                                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                                    '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산명</label>                                                   '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                                     '
        + '        	<i class="fa"></i>                                                                                                                  '
		+ '			<input type="text" id="name" name="name" class="form-control col-md-7 col-xs-12">                                                   '
        + '        </div>                                                                                                                               '
        + '    </div>                                                                                                                                   '
        + '</div>                                                                                                                                       '
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                                  '
        + '    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">                                                                                  '
        + '        <label class="control-label col-md-3 col-sm-3 col-xs-12">                                                                            '
        + '        	<span>                                                                                                                              '
        + '        		<b>[계좌정보]</b>                                                                                                               '
        + '        	</span>                                                                                                                             '
        + '        </label>                                                                                                                             '
        + '    </div>                                                                                                                                   '
        + '</div>                                                                                                                                       '
        + '<div class="col-md-12 col-sm-12 col-xs-12" id="accDiv">                                                                                      '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                                      '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">은행명</label>                                                   '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                                     '
        + '        	<i class="fa"></i>                                                                                                                  '
		+ '             <select class="form-control isSelectValid" id="bankCd" name="bankCd">                                                           '
		+ '                 <option value="">선택</option>                                                                                              '
        + '             </select>                                                                                                                       '
        + '        </div>                                                                                                                               '
        + '    </div>                                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                                    '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12 input-icon left">계좌번호</label>                                 '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                                     '
        + '        	<i class="fa"></i>                                                                                                                  '
		+ '			<input type="text" id="bankAccNo" name="bankAccNo" class="form-control col-md-7 col-xs-12">                                         '
        + '        </div>                                                                                                                               '
        + '    </div>                                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                                      '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">예금주</label>                                                   '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                                     '
        + '        	<i class="fa"></i>                                                                                                                  '
		+ '			<input type="text" id="bankHolder" name="bankHolder" class="form-control col-md-7 col-xs-12">                                       '
        + '        </div>                                                                                                                               '
        + '    </div>                                                                                                                                   '
        + '</div>                                                                                                                                       '
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                                  '
        + '    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">                                                                                  '
        + '        <label class="control-label col-md-3 col-sm-3 col-xs-12"><b>[거래처 담당자정보]</b></label>                                          '
        + '    </div>                                                                                                                                   '
        + '</div>                                                                                                                                       '
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                                  '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                                      '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자</label>                                               '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                                     '
        + '        	<i class="fa"></i>                                                                                                                  '
		+ '			<input type="text" id="billingNm" name="billingNm" class="form-control col-md-7 col-xs-12">                                         '
        + '        </div>                                                                                                                               '
        + '    </div>                                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                                    '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자 연락처</label>                                        '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                                     '
		+ '			<input type="text" id="billingTel" name="billingTel" class="form-control col-md-7 col-xs-12" isTel="true">                                       '
        + '        </div>                                                                                                                               '
        + '    </div>                                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                                      '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자 이메일</label>                                        '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left">                                                     '
        + '        	<i class="fa"></i>                                                                                                                  '
		+ '			<input type="text" id="billingEmail" name="billingEmail" class="form-control col-md-7 col-xs-12">                                   '
        + '        </div>                                                                                                                               '
        + '    </div>                                                                                                                                   '
        + '</div>                                                                                                                                       '
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                                  '
        + '    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">                                                                                  '
        + '        <label class="control-label col-md-3 col-sm-3 col-xs-12"><b>[KPC 담당자정보]</b></label>                                             '
        + '    </div>                                                                                                                                   '
        + '</div>                                                                                                                                       '
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                                  '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                                      '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자</label>                                               '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline ">                                                                    '
		+ '			<input type="text" id="kpcBillingNm" name="kpcBillingNm" class="form-control col-md-7 col-xs-12">       '
        + '        </div>                                                                                                                               '
        + '    </div>                                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                                    '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자 연락처</label>                                        '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                                     '
		+ '			<input type="text" id="kpcBillingTel" name="kpcBillingTel" class="form-control col-md-7 col-xs-12" isTel="true">    '
        + '        </div>                                                                                                                               '
        + '    </div>                                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                                      '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산담당자 이메일</label>                                        '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline ">                                                                    '
		+ '			<input type="text" id="kpcBillingEmail" name="kpcBillingEmail" class="form-control col-md-7 col-xs-12" >'
        + '        </div>                                                                                                                               '
        + '    </div>                                                                                                                                   '
        + '</div>                                                                                                                                       '
        + '<div class="col-md-12 col-sm-12 col-xs-12">                                                                                                  '
        + '    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">                                                                                  '
        + '        <label class="control-label col-md-3 col-sm-3 col-xs-12"><b>[정산정보]</b></label>                                                   '
        + '    </div>                                                                                                                                   '
        + '</div>                                                                                                                                       '
        + '<div class="col-md-12 col-sm-12 col-xs-12" id="billingDiv">                                                                                                  '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                                      '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">거래구분</label>                                                 '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline ">                                                                    '
        + '            <select class="form-control" id="divider" name="divider" >                                                                       '
        + '            </select>                                                                                                                        '
        + '        </div>                                                                                                                               '
        + '    </div>                                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                                    '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산 구분</label>                                                '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                                     '
        + '            <select class="form-control" id="code" name="code" >                                                                             '
        + '            </select>                                                                                                                        '
        + '        </div>                                                                                                                               '
        + '    </div>                                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                                      '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산주기</label>                                                 '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline ">                                                                    '
        + '            <select class="form-control" id="billingDuration" name="billingDuration" >                                                       '
        + '            </select>                                                                                                                        '
        + '        </div>                                                                                                                               '
        + '    </div>                                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                                    '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산일</label>                                                   '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline custom-input-icon left">                                              '
		+ '			<i>D+</i>                                                                                                                           '
		+ '			<input type="text" id="billingDt" name="billingDt" class=" col-lg-3 col-md-5 col-xs-12" >                                           '
        + '        </div>                                                                                                                               '
        + '    </div>                                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                                      '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산 수수료 타입</label>                                         '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                                     '
        + '			<select class="form-control" id="merchantCommType" name="merchantCommType" >                                                        '
        + '            </select>                                                                                                                        '
        + '        </div>                                                                                                                               '
        + '    </div>                                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                                    '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산 수수료</label>                                              '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left ">                                                    '
        + '        <i class="fa"></i>																													'
        + '            <input type="text" id="merchantCommision" name="merchantCommision" class="form-control input-xsmall">                            '
        + '            <span id="updateMerchantCommisionCurrency"></span>                            '
        + '        </div>                                                                                                                               '        
        + '    </div>                                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                                      '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">정산 타입</label>                                                '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline input-icon left ">                                                    '
        + '			<select class="form-control" id="billingCommType" name="billingCommType" >                                                        '
        + '            </select>                                                                                                                        '
        + '        </div>                                                                                                                               '
        + '    </div>                                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">                                    '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">수수료변경 적용일자</label>                                      '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">                                                                     '
        + '        <input type="text" class="form-control input-date-picker" id="aplEndDate" name="aplEndDate" >                                        '
        + '        </div>                                                                                                                               '
        + '    </div>                                                                                                                                   '
        + '    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">                                      '
        + '        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12">부가세 타입</label>                                              '
        + '        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline ">                                                                    '
        + '			<select class="form-control" id="merchantTaxType" name="merchantTaxType" >                                                          '
        + '            </select>                                                                                                                        '
        + '        </div>                                                                                                                               '
        + '    </div>                                                                                                                                   '
        + '</div>                                                                                                                                       '
        + '<div class="col-lg-12"><br /><span class="red" id="msgSpan"></span></div>'
        + '</form>'                                                                                                                                     
        + '</div><br />';
        
	var buttonHtml = '<button type="button" class="dt-button btn green btn-outline historyBtn">History</button>'
		           + '<button type="button" class="dt-button btn green btn-outline commFlag">수수료수정</button>'
				   + '<button type="button" class="dt-button btn green btn-outline btnSave">수정</button>';
	kpcUtil.openCommonPopup({
		modalTitle : "정산 수정",
		bodyHtml : bodyHtml,
		button : buttonHtml,
		modalSize : "modal-full",
		buttonEvent : [
			// 대표 거래처 수정 이벤트
   			{
   				target : ".btnSave",
   				eventType : "click",
   				callBack : function (){
   					if($("#billingUptForm").valid() && kpcUtil.confirm("승인 신청 하시겠습니까?") ){
   						kpcUtil.setFormDisable("#billingUptForm #billingDiv" , false);
                    	var menuId = "MCM-0003";
                    	// 승인자 선택
                    	kpcPopupUtil.openApprListPop({
                    		 menuId : menuId 
                    		,callBack : function (data){
                    			var apprEmpId = $("input[name=empList]:checked").attr("empId");
                    			console.log(apprEmpId);
   			   					if(typeof apprEmpId === "undefined"){
   			   						kpcUtil.customAlert("승인자를 선택해주세요.");
   			   						return false;
   			   					} else {
   			   						console.log(aplEndDate);
   			   						var jsonData = $("#billingUptForm").serializeJsonObject();
   			   						jsonData["apprEmpId"] = apprEmpId;
   			   						jsonData["menuId"] = menuId;
       			                    $.ajax({
       		                           url: "/api/merchants/services/service/billing",
       		                           data: JSON.stringify(jsonData),
       		                           type: 'PUT',
       		                           dataType : "json",
       		                           contentType  : "application/json",
       		                    	}).done(function(resultData,status,jqXhr){
       		                    		if(kpcUtil.successHandling("#billingUptForm",resultData,true)){
       		                    			$(".modal").modal('toggle');
       		                    		}
       		                        }).fail(function(e){
       		                	    	kpcUtil.errorHandling(e);
       		               	        });
   			   					}
                    		}
                    	});      				   						
   					}
   				}
   			},
   			// 모달 이벤트
   			{
   				target : ".modal",
   				eventType : "shown.bs.modal",
   				callBack : function (){
   					kpcUtil.setDatePicker("#aplEndDate");
   					kpcUtil.setFormDisable("#billingUptForm #billingDiv" , true);
   					setBillingFormValidate();
   					setBillingCommonCode(serviceBillingId);
					kpcUtil.setFormTextFieldFormat({
						target : "#billingUptForm"
					});					   					
   				}
   			},
   			{
   				target : ".commFlag",
   				eventType : "click",
   				callBack : function (){
   					if(kpcUtil.confirm("정산정보를 수정하시겠습니까?"))
   						kpcUtil.setFormDisable("#billingUptForm #billingDiv" , false);
   						$("#aplEndDate").focus().on("apply.daterangepicker" ,function (){
   							var m = new moment($(this).val());
   							var str = m.year() + "년 " + (m.month() +1) + " 월" + m.date() + " 일 00시부터 변경된 수수료 적용 예정 입니다."
   							$("#msgSpan").text(str);
   						});
   				}
   			},       			
   			{
   				target : ".historyBtn",
   				eventType : "click",
   				callBack : function (){
			   		kpcPopupUtil.openSecondPopup({
			   			modalTitle : "정산 수정 이력",
			   			modalSize : "modal-full",
			   			modalType : "URL",
			   			URL : "/approval/merchant/submerchant/billing/historyPop?historyType=APPR-0401",
			   			method : "GET",		   			
			   		});					          
   				}
   			},
   			{
   				target: "#merchantCommType",
   				eventType: "change",
   				callBack: function() {
   	            	$("#merchantCommType").change(function(event) {
   	            		//FEE-0001 = 비율정산, FEE-0002 = 건당
   	            		switch(event.target.value) {
   		            		case "FEE-0001":
   		            			$("#updateMerchantCommisionCurrency").text("%")
   		            			break;
   		            		case "FEE-0002":
   		            			$("#updateMerchantCommisionCurrency").text("원")
   		            			break;
   		            		default:
   		            			$("#updateMerchantCommisionCurrency").text("")
   	            		}
   	            	})
   				}
   			}
		]
	});
}

function getBillingData(serviceBillingId){
	$.ajax({
        url: "/api/merchants/services/service/billing",
        data : "serviceBillingId=" + serviceBillingId,
        type: 'GET',
        dataType : "json",
        contentType  : "application/json",
	}).done(function(data){
		var merchantCommisionCurrency = "";
		switch(data.merchantCommType) {
			case "FEE-0001":
				merchantCommisionCurrency = "%"
				break;
			case "FEE-0002":
				merchantCommisionCurrency = "원"
				break;
			default:
				merchantCommisionCurrency = "";
		}
		$("#updateMerchantCommisionCurrency").text(merchantCommisionCurrency)
    	kpcUtil.setFormData("#billingUptForm" , data);
    	var aplEndDt = kpcUtil.nullToBlank(data.aplEndDt);
    	if(aplEndDt != ""){
    		try{
    			$("#msgSpan").text(kpcUtil.setDateFormat(aplEndDt , "YYYY년 MM월 DD일") + " 적용 대기중인 수수료 변경 건이 있습니다.(수수료 : "+data.expectedMerchantCommision+merchantCommisionCurrency+")");
    		}catch(e){}
    	}
    	$("#billingUptForm").valid();
    }).fail(function(e){
        	kpcUtil.errorHandling(e);
    });	
}
var setBillingFormValidate = function (){
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

var setBillingCommonCode = function (serviceBillingId){
	
	kpcUtil.setSelectBoxData({
		target : [
		          "#billingUptForm #divider",
		          "#billingUptForm #code", 
		          "#billingUptForm #billingDuration",
		          "#billingUptForm #merchantCommType", 
		          "#billingUptForm #merchantTaxType", 
		          "#billingUptForm #bankCd",
		          "#billingUptForm #billingCommType"
		], 
		apiUrl : "/api/systemMng/common/commonCodeList",
		params : {type : 'DEAL,BIL,BILC,FEE,TAX,BANK,BILT'},
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
			getBillingData(serviceBillingId)
		}
	});
	
	
}