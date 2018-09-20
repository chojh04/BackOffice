/**
 * Created by sanghyun on 2017-02-10.
 * 오류 코드 정의
 * ####
 * # 성공 관련 코드
 * S001 [successHandling] 호출 오류 
 * ####
 * # 오류 관련 코드
 * E001 호출 폼데이터 설정중 발생 오류
 * E002 ajax호출중 발생 오류 
 */

$(document).ready(function (){
    // jquery validate 사업자 번호 체크 추가 
	$.validator.addMethod("bznoCheck", function (value,element){
		return this.optional(element) || kpcUtil.checkBizID(value);
	},"잘못된 사업자 등록번호입니다.");
	
	// jquery validate 사업자 번호 중복체크 
	$.validator.addMethod("bznoDupCheck", function (value,element){
		var returnVal;
		var result = $.ajax({
            url: "/api/merchants/merchant/bznoCheck",
            data: "bizRegNo=" + value ,
            type: 'GET',
            dataType : "json",
            contentType  : "application/json",
            async : false,
        });
		
		result.done(function(data){
			returnVal = (data.cnt > 0) ? false : true;
	    }).fail(function (data){
	    	returnVal = false;
	    })
	    ;
		return returnVal;
        
	},"중복된 사업자 등록번호입니다.");
	
	// jquery validate 연동 아이디 체크 
	$.validator.addMethod("svcConnIdDupCheck", function (value,element){
		var returnVal;
		var result = $.ajax({
            url: "/api/merchants/merchant/svcConnIdCheck",
            data: "svcConnIdCheck=" + value ,
            type: 'GET',
            dataType : "json",
            contentType  : "application/json",
            async : false,
        });
		
		result.done(function(data){
			returnVal = (data.cnt > 0) ? false : true;
	    });
		return returnVal;
        
	},"중복된 연동 ID 입니다.");	
	
	// jquery validate 법인 번호 중복체크 
	$.validator.addMethod("corpDupCheck", function (value,element){
		var returnVal;
		var result = $.ajax({
			url: "/api/merchants/merchant/corpNoCheck",
			data: "corpRegNo=" + value ,
			type: 'GET',
			dataType : "json",
			contentType  : "application/json",
			async : false,
		});  		
		result.done(function(data){
			returnVal = (data.cnt > 0) ? false : true;
		});
		return returnVal;
	},"중복된 법인 등록번호입니다.");
	
	// 비밀번호 체크
	$.validator.addMethod("passwordCheck", function (value,element){
		var returnVal;
		var result = $.ajax({
            url: "/api/user/passwordCheck",
            data: JSON.stringify({"pwd" : value}),
            type: 'POST',
            dataType : "json",
            contentType  : "application/json",
            async : false,
        });
		result.done(function(resultData){
			returnVal = resultData.data == "1"? true : false;
		});
		return returnVal;
        
	},"잘못된 비밀번호 입니다.");
	
	// 비밀번호 유효성 체크 
	$.validator.addMethod("passwordValidateCheck", function (value,element){
		
		var validate = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]/;
		return validate.test(value);
		
	},"비밀번호를 1자리이상의 특수문자를 포함하여 주세요.");	
	
	// TODO :  bootstrap select2의 경우 jquery validate의 change이벤트가 적용안됨 수정적용
	$(".isSelectValid").on("change" , function (){
		$(this).valid();
	});	
	
	jQuery.fn.serializeObject = function() {
	    var obj = null;
	    try {
	    	var tagName = this[0].tagName;
	        // this[0].tagName이 form tag일 경우
	        if(typeof this[0] !== "undefined" && 
	    		tagName && 
	    		(tagName.toUpperCase() == "DIV" || tagName.toUpperCase() == "FORM") ) {
	            var arr = $(this).find('input,select,checkbox,textarea').serializeArray();
	            if(arr){
	                obj = {};
	                jQuery.each(arr, function() {
	                	var key = this.name + "";
	                	if(obj.hasOwnProperty(key)){
	                		obj[key] = obj[key] + "," + this.value;
	                	}else {
	                		obj[key] = this.value;
	                	}
	                });
	                $(this).find("input[type=checkbox]").each(function (){
	                	obj[key] = this.value;
	                });
	            }
	        }
	    }catch(e) {
	        console.error(e.message);
	    }finally  {}
	    return JSON.stringify(obj);

	};
	
	jQuery.fn.serializeJsonObject = function() {
	    var obj = null;
	    try {
	    	var tagName = this[0].tagName;
	        // this[0].tagName이 form tag일 경우
	        if(typeof this[0] !== "undefined" && 
	    		tagName && 
	    		(tagName.toUpperCase() == "DIV" || tagName.toUpperCase() == "FORM") ) {
	            var arr = $(this).find('input,select,checkbox,textarea').serializeArray();
	            if(arr){
	                obj = {};
	                jQuery.each(arr, function() {
	                	var key = this.name + "";
	                	if(obj.hasOwnProperty(key)){
	                		obj[key] = obj[key] + "," + this.value;
	                	}else {
	                		obj[key] = this.value;
	                	}
	                });
	                $(this).find("input[type=checkbox]").each(function (){
	                	obj[key] = this.value;
	                });
	            }
	        }
	    }catch(e) {
	        console.error(e.message);
	    }finally  {}
	    return obj;

	};	
	
	String.prototype.removeComma = function () {
		return this.replace(/,/g, "");
	};
	
	String.prototype.addComma = function () {
	    return this.replace(/\B(?=(\d{3})+(?!\d))/g, "," );
	};

	// navigation 시작
    var CURRENT_URL = window.location.href.split('?')[0];
    // Sidebar
    // TODO: This is some kind of easy fix, maybe we can improve this
    $('#sidebar-menu').find("a").on('click', function(ev) {

        var $li = $(this).parent();

        if ($li.is('.active')) {
            $li.removeClass('active active-sm');
            $('ul:first', $li).slideUp(function() {
                kpcUtil.setContentHeight();
            });
        } else {
            // prevent closing menu if we are on child menu
            if (!$li.parent().is('.child_menu')) {
                $('#sidebar-menu').find('li').removeClass('active active-sm');
                $('#sidebar-menu').find('li ul').slideUp();
            }

            $li.addClass('active');

            $('ul:first', $li).slideDown(function() {
                kpcUtil.setContentHeight();
            });
        }
    });

    // check active menu
    $('#sidebar-menu').find('a[href="' + CURRENT_URL + '"]').parent('li').addClass('current-page');

    $('#sidebar-menu').find('a').filter(function() {
        return this.href == CURRENT_URL;
    }).parent('li').addClass('current-page').parents('ul').slideDown(function() {
        kpcUtil.setContentHeight();
    }).parent().addClass('active');


    // recompute content when resizing
    $(window).resize(function() {
        kpcUtil.setContentHeight();
    });

    // /Sidebar
    $('.collapse-link').on('click', function() {
        var $BOX_PANEL = $(this).closest('.x_panel'),
            $ICON = $(this).find('i'),
            $BOX_CONTENT = $BOX_PANEL.find('.x_content');

        // fix for some div with hardcoded fix class
        if ($BOX_PANEL.attr('style')) {
            $BOX_CONTENT.slideToggle(200, function() {
                $BOX_PANEL.removeAttr('style');
            });
        } else {
            $BOX_CONTENT.slideToggle(200);
            $BOX_PANEL.css('height', 'auto');
        }

        $ICON.toggleClass('fa-chevron-up fa-chevron-down');
    });

    $('.close-link').click(function() {
        var $BOX_PANEL = $(this).closest('.x_panel');

        $BOX_PANEL.remove();
    });
    // toggle small or large menu
    $('#menu_toggle').on('click', function() {

        if ($('body').hasClass('nav-md')) {
            $('#sidebar-menu').find('li.active ul').hide();
            $('#sidebar-menu').find('li.active').addClass('active-sm').removeClass('active');
        } else {
            $('#sidebar-menu').find('li.active-sm ul').show();
            $('#sidebar-menu').find('li.active-sm').addClass('active').removeClass('active-sm');
        }

        $('body').toggleClass('nav-md nav-sm');

        kpcUtil.setContentHeight();
    });
	// navigation 종료
    // 화면 자동 사이징
    kpcUtil.setContentHeight();
});


var kpcUtil = new function (){
	
	var merchantId = "";
	var merchantName = "";
	
	var subMerchantId = "";
	var subMerchantName = "";
	
	var serviceId = "";
	var serviceName = "";
	
	this.setServiceName = function (serviceName){
		this.serviceName = serviceName;     	
	}
    this.setServiceId = function (serviceId){
    	this.serviceId = serviceId;
    }
    
    this.setMerchantId = function (merchantId){
    	this.merchantId = merchantId;  
    }
    
    this.getServiceName = function (){
    	return this.serviceName;     	
    }
    this.getServiceId = function (){
    	return this.serviceId;     	
    }
    this.setMerchantName = function (merchantName){
    	this.merchantName = merchantName;
    }
    
    this.getMerchantId = function (){
    	return this.merchantId;  
    }
    
    this.getMerchantName = function (){
    	return this.merchantName;  
    }	
    
    this.setSubMerchantId = function (merchantId){
    	this.SubMerchantId = merchantId  
    }
    
    this.setSubMerchantName = function (merchantName){
    	this.SubMerchantName = merchantName     	
    }
    this.getSubMerchantId = function (){
    	return this.SubMerchantId;  
    }
    
    this.getSubMerchantName = function (){
    	return this.SubMerchantName;  
    }	
    
    this.nullToBlank = function (str){
    	if (typeof str === "undefined" || str === "" || str == null || str === "null"){
    		return "";
    	}
    	return str;
    }
    
	this.checkBizID = function(bizID){
		var checkID = new Array(1, 3, 7, 1, 3, 7, 1, 3, 5, 1);
		var tmpBizID , i , chkSum=0, c2 , remander;
		bizID = bizID.replace(/-/gi , '');
		
		for (i = 0; i <= 7; i ++) chkSum += checkID[i] * bizID.charAt(i);
		c2 = "0" + (checkID[8] * bizID.charAt(8));
		c2 = c2.substring(c2.length - 2 , c2.length);
		chkSum += Math.floor(c2.charAt(0)) + Math.floor(c2.charAt(1));
		remander = (10 - (chkSum %10)) %10;
		if(Math.floor(bizID.charAt(9)) == remander) return true;
		return false;
	}	
	
    this.setContentHeight = function () {
        var contentHeight = $(window).height() - ($('.nav_menu').height() + $('footer').height()) + 24;
        $('.right_col').css('min-height', contentHeight);
        
    }

    this.setDynamicInputBySelectBox= function($select){
        var selectedVal = $select.val();
        $select.parent().find("input").each(function (){
            if($(this).attr("name") === selectedVal){
              $(this).removeClass("hidden");
            }else{
              $(this).addClass("hidden");
            }
        });
    }

    this.getDateOption = function(date) {
        return {
            singleDatePicker: true,
            calender_style: "picker_2",
            startDate : date,
            autoUpdateInput : false,
            showDropdowns: true,
            "locale": {
                "format": "YYYY-MM-DD",
                "separator": " - ",
                "applyLabel": "Apply",
                "cancelLabel": "Clear",
                "fromLabel": "From",
                "toLabel": "To",
                "customRangeLabel": "Custom",
                "weekLabel": "W",
                daysOfWeek: ['일', '월', '화', '수', '목', '금', '토'],
                monthNames: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
            }
        }
    }
    
    this.getDateOptionToday = function(date) {
    	return {
    		singleDatePicker: true,
    		calender_style: "picker_2",
    		startDate : date,
    		autoUpdateInput : true,
    		showDropdowns: true,
    		"locale": {
    			"format": "YYYY-MM-DD",
    			"separator": " - ",
    			"applyLabel": "Apply",
    			"cancelLabel": "Clear",
    			"fromLabel": "From",
    			"toLabel": "To",
    			"customRangeLabel": "Custom",
    			"weekLabel": "W",
    			daysOfWeek: ['일', '월', '화', '수', '목', '금', '토'],
    			monthNames: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
    		}
    	}
    }
    
    this.getRangeDateOption = function(date) {
        return {
            "startDate" : kpcUtil.getFirstday(),
            "endDate" : date,
            "showDropdowns" : true,
            "locale": {
                "format": "YYYY-MM-DD",
                "separator": " - ",
                "applyLabel": "Apply",
                "cancelLabel": "Clear",
                "fromLabel": "From",
                "toLabel": "To",
                daysOfWeek: ['일', '월', '화', '수', '목', '금', '토'],
                monthNames: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
            }
        }
    }    
    
    this.getRangeDateTimeOption = function(date) {
        return {
            "startDate" : kpcUtil.getFirstday(),
            "endDate" : kpcUtil.getTodayTime(),
            "showDropdowns" : true,
            "timePicker" : true,
            "timePicker24Hour" : true,
            "locale": {
                "format": "YYYY-MM-DD HH:mm",
                "separator": " - ",
                "applyLabel": "Apply",
                "cancelLabel": "Clear",
                "fromLabel": "From",
                "toLabel": "To",
                daysOfWeek: ['일', '월', '화', '수', '목', '금', '토'],
                monthNames: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
            }
        }
    }     
    
    this.getRangeDateStartDateOption = function(date) {
        return {
            "startDate" : date,
            "endDate" : kpcUtil.getTodayTime(),
            "maxDate" : kpcUtil.getTodayTime(),
            "showDropdowns" : true,
            "timePicker" : true,
            "timePicker24Hour" : true,
            "locale": {
                "format": "YYYY-MM-DD",
                "separator": " - ",
                "applyLabel": "Apply",
                "cancelLabel": "Clear",
                "fromLabel": "From",
                "toLabel": "To",
                daysOfWeek: ['일', '월', '화', '수', '목', '금', '토'],
                monthNames: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
            }
        }
    }
    
    this.setStartEndDateRange = function(startDate, endDate) {
    	return {
    		"startDate" : startDate,
    		"endDate" : endDate,
    		"maxDate" : kpcUtil.getTodayTime(),
    		"showDropdowns" : true,
    		"timePicker" : true,
    		"timePicker24Hour" : true,
    		"locale": {
    			"format": "YYYY-MM-DD",
    			"separator": " - ",
    			"applyLabel": "Apply",
    			"cancelLabel": "Clear",
    			"fromLabel": "From",
    			"toLabel": "To",
    			daysOfWeek: ['일', '월', '화', '수', '목', '금', '토'],
    			monthNames: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
    		}
    	}
    }
    
    
    
    
    this.setDatePicker = function (inputId){
    	var todayDateOption = kpcUtil.getDateOption(kpcUtil.getToday());
    	$(inputId).daterangepicker(todayDateOption)
		.on('cancel.daterangepicker', function (ev,picker) {
			$(this).val('');
		})
		.on('apply.daterangepicker', function (ev,picker) {
			$(this).val(picker.startDate.format('YYYY-MM-DD'));
		});
    }
    
    this.setDatePickerToday = function (inputId){
    	var todayDateOption = kpcUtil.getDateOptionToday(kpcUtil.getToday());
    	$(inputId).daterangepicker(todayDateOption)
    	.on('cancel.daterangepicker', function (ev,picker) {
    		$(this).val('');
    	})
    	.on('apply.daterangepicker', function (ev,picker) {
    		$(this).val(picker.startDate.format('YYYY-MM-DD'));
    	});
    }
    
    this.setDateRangePicker = function (inputId){
    	var todayDateOption = kpcUtil.getRangeDateOption(kpcUtil.getToday());
    	$(inputId).daterangepicker(todayDateOption)
    	.on('cancel.daterangepicker', function (ev,picker) {
    		$(this).val('');
    	})
    	.on('apply.daterangepicker', function (ev,picker) {
    		$(this).val(picker.startDate.format('YYYY-MM-DD') + " - " + picker.endDate.format('YYYY-MM-DD'));
    	});
    }
    
    this.setDateRangePickerEndDateIsYesterday = function (inputId){
    	var yesterdayDateOption = kpcUtil.getRangeDateOption(kpcUtil.getYesterday());
    	$(inputId).daterangepicker(yesterdayDateOption)
    	.on('cancel.daterangepicker', function (ev,picker) {
    		$(this).val('');
    	})
    	.on('apply.daterangepicker', function (ev,picker) {
    		$(this).val(picker.startDate.format('YYYY-MM-DD') + " - " + picker.endDate.format('YYYY-MM-DD'));
    	});
    }
    
    this.setDateRangeStartDateOptionPicker = function (inputId, date){
    	var todayDateOption = kpcUtil.getRangeDateStartDateOption(date);
    	$(inputId).daterangepicker(todayDateOption)
    	.on('cancel.daterangepicker', function (ev,picker) {
    		$(this).val('');
    	})
    	.on('apply.daterangepicker', function (ev,picker) {
    		$(this).val(picker.startDate.format('YYYY-MM-DD') + " - " + picker.endDate.format('YYYY-MM-DD'));
    	});
    }
    
    this.setStartEndDateRangePicker = function (inputId, startDate, endDate){
    	$(inputId).daterangepicker(kpcUtil.setStartEndDateRange(startDate, endDate))
    	.on('cancel.daterangepicker', function (ev,picker) {
    		$(this).val('');
    	})
    	.on('apply.daterangepicker', function (ev,picker) {
    		$(this).val(picker.startDate.format('YYYY-MM-DD') + " - " + picker.endDate.format('YYYY-MM-DD'));
    	});
    }
    
    

    this.setDateTimeRangePicker = function (inputId){
    	var todayDateOption = kpcUtil.getRangeDateTimeOption(kpcUtil.getToday());
    	$(inputId).daterangepicker(todayDateOption)
    	.on('cancel.daterangepicker', function (ev,picker) {
    		$(this).val('');
    	})
    	.on('apply.daterangepicker', function (ev,picker) {
    		$(this).val(picker.startDate.format('YYYY-MM-DD HH:mm') + " - " + picker.endDate.format('YYYY-MM-DD HH:mm'));
    	});
    }    
    
    this.getToday = function (){
        return moment(new Date).format("YYYY-MM-DD");
    }
    
    this.getYesterday = function (){
        return moment(new Date).subtract(1, 'days').format("YYYY-MM-DD");
    }
    
    this.getFirstday = function (){
        return moment(new Date).format("YYYY/MM") + "/01";
    }
    
    this.getTodayTime = function (){
    	return moment(new Date).format("YYYY-MM-DD") + " 23:59";
    }
    
    this.intVal = function (i) {
        var returnData;
        returnData = typeof i === 'string' ? i.replace(/,/g, '') : typeof i === 'number' ? i : 0;
        return returnData * 1;
    }    
    
    this.numberWithCommas = function (x) {
    	if(typeof x === "undefined" || x == null){
    		return "";
    	}
    	var parts = x.toString().split(".");
   		return parts[0].toString().replace(/\B(?=(\d{3})+(?!\d))/g,",") + (parts[1]? "." + parts[1] : "");
    }
    
    this.setDateFormat = function (str , format){
    	if(typeof str === "undefined" || str == null || str === ""){
    		return "";
    	}
    	return moment(str).format(format);
    }
    
    this.setAllChecked = function (objId){
        if(typeof objId !== "string"){
            return false;
        }    	
    	var $obj = $(objId);
    	$obj.change(function (){
    		var checked = $(this).is(":checked");
        	$($(this).attr("data-set")).each(function (){
        		var tagName = $(this).get(0).tagName;
        		if (checked && (tagName === "TD" || tagName === "INPUT")){
        			$(this).prop("checked" , true);
        		} else {
        			$(this).prop("checked" , false);
        		}
        	});
        });
    }
     

    /**
     * 폼의 모든 요소를 초기화한다.
     * @author sanghyun
     * @date 2017. 03. 21.
     * @content 
     * @version 1.0
     * @param formObj
     * @returns
     */
    this.resetForm = function (formName){
        // select input textarea
        if(typeof formName !== "string"){
           return false;
        }
		var thisform = $(formName).closest('form');
	    thisform.each(function (){
	      this.reset();
	      $(this).validate().resetForm();
	    });
	    thisform.find('select,div,i,span').each(function (){
	    	var tagName = $(this).prop("tagName");
	    	if(tagName === "SELECT"){
				$(this).find('option:selected').removeAttr('selected');
				$(this).val($(this).find("option:first").val());
				$(this).change();
    		} else if(tagName === "DIV" || tagName === "I"){
				$(this).removeClass("has-error")
					   .removeClass("fa-warning")
					   .removeClass("fa-check")
					   .removeClass("has-success")
					   ;
    		} 
		});    
    } // end function resetForm
    
    /**
     * form + span 초기화 모든 요소를 초기화한다.
     * @author sanghyun
     * @date 2017. 04. 28.
     * @content 
     * @version 1.0
     * @param formObj
     * @returns
     */
    this.resetSpanForm = function (formName){
    	// select input textarea
    	if(typeof formName !== "string"){
    		return false;
    	}
    	var thisform = $(formName).closest('form');
    	thisform.each(function (){
    		this.reset();
    		$(this).validate().resetForm();
    	});
    	thisform.find('select,div,i,span').each(function (){
    		var tagName = $(this).prop("tagName");
    		if(tagName === "SELECT"){
    			$(this).find('option:selected').removeAttr('selected');
    			$(this).val($(this).find("option:first").val());
    			$(this).change();
    		} else if(tagName === "DIV" || tagName === "I"){
    			$(this).removeClass("has-error")
    			.removeClass("fa-warning")
    			.removeClass("fa-check")
    			.removeClass("has-success")
    			;
    		} else if (tagName === "SPAN"){
    			$(this).text('');    			
    		}
    	});    
    } // end function resetForm

    /**
     * 폼의 모든 요소를 초기화한다.
     * @author sanghyun
     * @date 2017. 03. 21.
     * @content 
     * @version 1.0
     * @param formObj
     * @returns
     */
    this.resetDiv = function (formName){
        // select input textarea
        if(typeof formName !== "string"){
           return false;
        }
		var thisform = $(formName);
	    thisform.find("input,select,textarea").each(function (){
	      $(this).val('');
	      $(this).validate().resetForm();
	    });
	    thisform.find('select,div,i,span').each(function (){
	    	var tagName = $(this).prop("tagName");
	    	if(tagName === "SELECT"){
				$(this).find('option:selected').removeAttr('selected');
				$(this).val($(this).find("option:first").val());
				$(this).change();
    		} else if(tagName === "DIV" || tagName === "I"){
				$(this).removeClass("has-error")
					   .removeClass("fa-warning")
					   .removeClass("fa-check")
					   .removeClass("has-success")
					   ;
    		} 
		});    
    } // end function resetForm
    
    this.setBznoFormat = function (_val){
    	var val = kpcUtil.nullToBlank(_val).replace(/-/gi , '');
    	if(val.length < 5){
    		return val;
    	}
    	return val.substring(0,3) + "-" + val.substring(3,5) + "-" + val.substring(5);
    }
    
    this.replaceHyphen = function (_val){
		return kpcUtil.nullToBlank(_val).replace(/-/gi , '');
    }     
    this.setTelFormat = function (_val){
    	var val = kpcUtil.nullToBlank(_val).replace(/-/gi , '');
    	if(val != ""){
			if(val.length == 7){
			  val = val.substring(0,3) + "-" + val.substring(3) ;
			} else if(val.length == 8){
			  val = val.substring(0,4) + "-" + val.substring(4) ;
			} else if(val.length == 9){
			  val = val.substring(0,2) + "-" + val.substring(2,5) + "-" + val.substring(5) ; 
			} else if(val.length == 10){
			  if(val.substring(0,2) == "02"){
				  val = val.substring(0,2) + "-" + val.substring(2,6) + "-" + val.substring(6)  ;
			  } else {
				  val = val.substring(0,3) + "-" + val.substring(3,6) + "-" + val.substring(6);
			  }
			} else if(val.length == 11){
				val = val.substring(0,3) + "-" + val.substring(3,7) + "-" + val.substring(7);
			}
    	}
		return val;
    } 
    
    /**
     * json data를 form에 자동 셋팅한다.
     * @author sanghyun
     * @date 2017. 03. 21.
     * @content 
     * @version 1.0
     * @param formName (ex : #폼명)
     * @param data (ex : json ) 
     * @returns
     */
    this.setFormData = function(formName , data){
       // select input textarea
       if(typeof formName !== "string"){
          return false;
       }
       $(formName).find("input,select,textarea,span").each(function (){
    	  var this_name = $(this).attr("name");
          if(typeof this_name === "undefined"){
        	  this_name = $(this).attr("id");
          }
          var input_type = $(this).attr("type");
          if(data.hasOwnProperty(this_name)){
        	  var _val = data[this_name];
        	  if (_val != undefined) {
        		  if($(this).attr("isNumber")){
        			  _val = kpcUtil.numberWithCommas(_val);
        		  } else if($(this).attr("isDateField")){
        			  _val = kpcUtil.setDateFormat(_val , "YYYY-MM-DD");
        		  } else if($(this).attr("isBzno")){
        			  if(_val.length > 0){
        				  _val = kpcUtil.setBznoFormat(_val);
        			  }
        		  } else if($(this).attr("isTel")){
        			  _val = kpcUtil.setTelFormat(_val); 
        		  }
        		  if(typeof _val !== "undefined"){
        			  var tagName = $(this).prop("tagName");
        			  if (tagName === "INPUT"){
        				  if(input_type === "checkbox"){
        					  if($(this).val() == _val){
        						  $(this).attr("checked" , true);   
        					  }
        				  }else if(input_type === "text"){
        					  $(this).val(_val).focusout();
        				  }else if(input_type === "radio"){
        					  if($(this).val() === _val){
        						  $(this).prop("checked" , true);
        					  }
        				  }else{
        					  $(this).val(_val).focusout();
        				  }
        			  }else if(tagName === "SELECT"){
        				  $(this).val(_val).change();
        			  }else if(tagName === "SPAN"){
        				  $(this).html(_val);
        			  }else {
        				  // TODO : 추가 작업필요
        				  $(this).val(_val).focusout();
        			  }
        		  } // end if ()
        	  }
          }
       }); // end each
       return true;
    } // end function
    
    this.errorHandling = function (e){
        if(e.status === 401){
        	kpcUtil.customAlert("세션이 만료 되었습니다.");
        	location.href ='/backOffice/login';
        }else{
        	console.error(e);
        	kpcUtil.customAlert("[E002]오류가 발생하였습니다. 관리자에게 문의하세요.\n"+ e.status + " , errorMsg : " + e.statusText);
        }
    }
    
    this.successHandling = function (formId,data, clearFlag){
    	console.log(data.status);
        if(this.httpCodeHandling(data.status)){
        	if (clearFlag) kpcUtil.resetForm(formId);
        	kpcUtil.customAlert("저장 되었습니다.");
        }else {
        	kpcUtil.customAlert("[S001]오류가 발생하였습니다. 관리자에게 문의하세요.\n"+ JSON.stringify(data));
        	return false;
        }
        return true;
    }
    
    this.successHandlingToMsg = function (formId,data, clearFlag,msg){
        if(this.httpCodeHandling(data.status)){
        	if (clearFlag) kpcUtil.resetForm(formId);
        	kpcUtil.customAlert(msg);
        }else {
        	kpcUtil.customAlert("[S001]오류가 발생하였습니다. 관리자에게 문의하세요.\n"+ JSON.stringify(data));
        	return false;
        }
        return true;
    }    
    
    this.successHandlingConfirm = function (obj){
        if(this.httpCodeHandling(obj.data.status)){
        	if (obj.clearFlag) kpcUtil.resetForm(obj.formId);
        	return kpcUtil.confirm(obj.msg);
        }else {
        	kpcUtil.customAlert("[S001]오류가 발생하였습니다. 관리자에게 문의하세요.\n"+ JSON.stringify(obj.data));
        	return "error";
        }
        return true;
    }    
    
    this.kpcApiSuccessHandling = function (formId, data, clearFlag){
    	if(data.code == "K206"){
    		kpcUtil.customAlert("일치하는 데이터가 없습니다.");
    		return false;
    	}else if(data.code != "K000"){
        	kpcUtil.customAlert("code:["+ kpcUtil.nullToBlank(data.code) +"]\nmessage:["+ kpcUtil.nullToBlank(data.message) + "]");
    		return false;
    	}
    	if (clearFlag) kpcUtil.resetForm(formId);
        return true;
    }    
    
    this.deleteHandling = function (data){
    	if(this.httpCodeHandling(data.status)){
    		kpcUtil.customAlert("삭제 되었습니다.");
    	}else {
    		kpcUtil.customAlert("[E002]오류가 발생하였습니다. 관리자에게 문의하세요.\n"+ JSON.stringify(data));
    		return false;
    	}
    	return true;
    }
    
    this.httpCodeHandling = function (code){
    	if(code == "200" || code == "201" || code == "OK"){
    		return true;
    	}
    	
    	return false;
    }
    
    /**
     * json data를 form에 셋팅한다.
     * @author sanghyun
     * @date 2017. 03. 21.
     * @content 
     * @version 1.0
     * @param modalId (ex : #폼명)
     * @param formId (ex : #폼명)
     * @param data (ex : json ) 
     * @returns
     */    
    this.setFormDataToModal = function (modalId , formId , data){
    	kpcUtil.resetForm(formId);
    	if(!kpcUtil.setFormData(formId , data)){
    		kpcUtil.customAlert("[E001]잘못된 데이터 입니다.\n관리자에게 문의 바랍니다.");
    		return;
    	}
    	$(modalId).modal({backdrop: 'static'});    	
    }

    this.setFormDisable = function(formName,flag){
        // select input textarea
        if(typeof formName !== "string"){
           return false;
        }
        $(formName).find("input,select,textarea").each(function (){
        	$(this).prop("disabled" , flag);
        });    // end each
        return true;
    } // end function
    
    this.setFormReadonly = function(formName,flag){
    	// select input textarea
    	if(typeof formName !== "string"){
    		return false;
    	}
    	$(formName).find("input,select,textarea").each(function (){
    		$(this).prop("readonly" , flag);
    	});    // end each
    	return true;
    } // end function
    
    this.confirm = function(msg){
    	return confirm(msg);
    } // end function
    
    this.customAlert = function(msg){
    	// TODO : 추후 bootstrap alert 으로 변경예정 
    	alert(msg);
    } // end function
    

    this.numberChk = function(data) {
    	//숫자만 입력    	
    	var inputVal = $(data).val();    	
    	$(data).val(inputVal.replace(/[^0-9]/gi,''));
    }

    
    this.getAjaxContent = function(url,params,type, target){
    	$.ajax({
    		mimeType : "text/html; charset=utf-8",
    		dataType : "html",
    		url : url,
    		data : params,
    		type : type,
    	}).done(function (data){
			$(target).html(data);
		}).fail(function  (xhr , status,  error){
			console.error(error);
	        if(xhr.status === 401){
	        	kpcUtil.customAlert("세션이 만료 되었습니다.");
	        	location.href = '/backOffice/login';
	        }
		});
    }
    
    this.setSelectBoxData = function(jsonData){
    	var target = jsonData.target;
    	var apiUrl = jsonData.apiUrl;
    	var params = jsonData.params;
    	var type   = jsonData.type;
    	var option = jsonData.option;
    	var callBack = jsonData.callBack;
    	$.ajax({
    		mimeType : "text/html; charset=utf-8",
    		dataType : "json",
    		url : apiUrl,
    		data : params,
    		type : type, 
    	}).done(function (resultData){
			callBack(resultData,target,option);
		}).fail(function  (xhr , status,  error){
			console.error(error);
	        if(xhr.status === 401){
	        	kpcUtil.customAlert("세션이 만료 되었습니다.");
	        	location.href = '/backOffice/login';
	        }
		});      	
    }

    this.openMerchantsPopup = function(merchantId , merchantName , nextTarget){
    	
    	if($("#merchantPopupModal").length == 0){
    		var html = ''
    			+ '<div class="modal fade" id="merchantPopupModal"  role="dialog" aria-labelledby="merchantPopupModalLabel">'
    			+ '    <div class="modal-dialog modal-lg" role="document">                                                  '
    			+ '        <div class="modal-content">                                                                      '
    			+ '            <div class="modal-header">                                                                   '
    			+ '                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span        '
    			+ '                        aria-hidden="true">&times;</span></button>                                       '
    			+ '                <h4 class="modal-title" id="merchantPopupModalLabel">상위 거래처 조회</h4>               '
    			+ '            </div>                                                                                       '
    			+ '            <div class="merchants-modal-body modal-body form">                                           '
    			+ '            	                                                                                            '
    			+ '            </div>                                                                                       '
    			+ '            <div class="modal-footer">                                                                   '
    			+ '                <button type="button" class="btn btn-default" data-dismiss="modal">닫기</button>         '
    			+ '            </div>                                                                                       '
    			+ '        </div>                                                                                           '
    			+ '    </div>                                                                                               '
    			+ '</div>     	                                                                                             ';
    		$(".right_col").append(html);
    	}
    	kpcUtil.setMerchantId("");
    	kpcUtil.setMerchantName("");
    	$("#merchantPopupModal").on("hidden.bs.modal" , function (){
    		$(merchantId).val(kpcUtil.getMerchantId());
    		$(merchantName).val(kpcUtil.getMerchantName());
    		$(merchantName).focus();
    		$(nextTarget).focus();
    	});
    	kpcUtil.getAjaxContent("/backOffice/common/popup/merchants","","GET",".merchants-modal-body");
    	$("#merchantPopupModal").modal({backdrop: 'static'});
    }
    
    this.openSubMerchantsPopup = function(merchantId , merchantName , nextTarget){
    	
    	if($("#subMerchantPopupModal").length == 0){
    		var html = ''
    			+ '<div class="modal fade" id="subMerchantPopupModal"  role="dialog" aria-labelledby="subMerchantPopupModalLabel">'
    			+ '    <div class="modal-dialog modal-lg" role="document">                                                  '
    			+ '        <div class="modal-content">                                                                      '
    			+ '            <div class="modal-header">                                                                   '
    			+ '                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span        '
    			+ '                        aria-hidden="true">&times;</span></button>                                       '
    			+ '                <h4 class="modal-title" id="merchantPopupModalLabel">일반 거래처 조회</h4>               '
    			+ '            </div>                                                                                       '
    			+ '            <div class="merchants-modal-body modal-body form">                                           '
    			+ '            	                                                                                            '
    			+ '            </div>                                                                                       '
    			+ '            <div class="modal-footer">                                                                   '
    			+ '                <button type="button" class="btn btn-default" data-dismiss="modal">닫기</button>         '
    			+ '            </div>                                                                                       '
    			+ '        </div>                                                                                           '
    			+ '    </div>                                                                                               '
    			+ '</div>     	                                                                                            ';
    		$(".right_col").append(html);
    	}
    	kpcUtil.setSubMerchantId("");
    	kpcUtil.setSubMerchantName("");
    	$("#subMerchantPopupModal").on("hidden.bs.modal" , function (){
    		$(merchantId).val(kpcUtil.getSubMerchantId());
    		$(merchantName).val(kpcUtil.getSubMerchantName());
    		$(merchantId).focus();
    		$(nextTarget).focus();
    	});
    	kpcUtil.getAjaxContent("/backOffice/common/popup/submerchants","","GET",".merchants-modal-body");
    	$("#subMerchantPopupModal").modal({backdrop: 'static'});
    }
    
    this.openServicePopup = function(serviceId , serviceName , nextTarget){
    	
    	if($("#servicePopupModal").length == 0){
    		var html = ''
    			+ '<div class="modal fade" id="servicePopupModal"  role="dialog" aria-labelledby="servicePopupModalLabel">'
    			+ '    <div class="modal-dialog modal-lg" role="document">                                                  '
    			+ '        <div class="modal-content">                                                                      '
    			+ '            <div class="modal-header">                                                                   '
    			+ '                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span        '
    			+ '                        aria-hidden="true">&times;</span></button>                                       '
    			+ '                <h4 class="modal-title" id="servicePopupModalLabel">서비스 조회</h4>               '
    			+ '            </div>                                                                                       '
    			+ '            <div class="service-modal-body modal-body form">                                           '
    			+ '            	                                                                                            '
    			+ '            </div>                                                                                       '
    			+ '            <div class="modal-footer">                                                                   '
    			+ '                <button type="button" class="btn btn-default" data-dismiss="modal">닫기</button>         '
    			+ '            </div>                                                                                       '
    			+ '        </div>                                                                                           '
    			+ '    </div>                                                                                               '
    			+ '</div>     	                                                                                            ';
    		$(".right_col").append(html);
    	}
    	kpcUtil.setServiceId("");
    	kpcUtil.setServiceName("");
    	$("#servicePopupModal").on("hidden.bs.modal" , function (){
    		$(serviceId).val(kpcUtil.getServiceId());
    		$(serviceName).val(kpcUtil.getServiceName());
    	});
    	kpcUtil.getAjaxContent("/backOffice/common/popup/services","","GET",".service-modal-body");
    	$("#servicePopupModal").modal({backdrop: 'static'});
    }    
    
    this.openFileUploadPopup = function(endpoint){
    	
    	if($("#fileUploadPopupModal").length == 0){
    		var html = ''
    			+ '<div class="modal fade" id="fileUploadPopupModal"  role="dialog" aria-labelledby="fileUploadPopupModal">'
    			+ '    <div class="modal-dialog modal-lg" role="document">                                                  '
    			+ '        <div class="modal-content">                                                                      '
    			+ '            <div class="modal-header">                                                                   '
    			+ '                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span        '
    			+ '                        aria-hidden="true">&times;</span></button>                                       '
    			+ '                <h4 class="modal-title" id="fileUploadPopupModalLabel">파일 업로드</h4>                  '
    			+ '            </div>                                                                                       '
    			+ '            <div class="merchants-modal-body modal-body form">                                           '
    		    + ' <link href="/bower_components/fine-uploader/fine-uploader-gallery.min.css" rel="stylesheet">                              '
    		    + ' <script src="/bower_components/fine-uploader/fine-uploader.min.js"></script>                                              '
    		    + ' <script type="text/template" id="qq-template">                                                          '
    		    + '     <div class="qq-uploader-selector qq-uploader qq-gallery" qq-drop-area-text="Drop files here">       '
    		    + '         <div class="qq-total-progress-bar-container-selector qq-total-progress-bar-container">          '
    		    + '             <div role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" class="qq-total-progress-bar-selector qq-progress-bar qq-total-progress-bar"></div>'
    		    + '         </div>                                                                                                                                             '
    		    + '         <div class="qq-upload-drop-area-selector qq-upload-drop-area" qq-hide-dropzone>                                                                    '
    		    + '             <span class="qq-upload-drop-area-text-selector"></span>                                                                                        '
    		    + '         </div>                                                                                                                                             '
    		    + '         <div class="qq-upload-button-selector qq-upload-button">                                                                                           '
    		    + '             <div>Upload a file</div>                                                                                                                       '
    		    + '         </div>                                                                                                                                             '
    		    + '         <span class="qq-drop-processing-selector qq-drop-processing">                                                                                      '
    		    + '             <span>Processing dropped files...</span>                                                                                                       '
    		    + '         <span class="qq-drop-processing-spinner-selector qq-drop-processing-spinner"></span>                                                               '
    		    + '         </span>                                                                                                                                            '
    		    + '         <ul class="qq-upload-list-selector qq-upload-list" role="region" aria-live="polite" aria-relevant="additions removals">                            '
    		    + '             <li>                                                                                                                                           '
    		    + '                 <span role="status" class="qq-upload-status-text-selector qq-upload-status-text"></span>                                                   '
    		    + '                 <div class="qq-progress-bar-container-selector qq-progress-bar-container">                                                                 '
    		    + '                     <div role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" class="qq-progress-bar-selector qq-progress-bar"></div>'
    		    + '                 </div>                                                                                                              '
    		    + '                 <span class="qq-upload-spinner-selector qq-upload-spinner"></span>                                                  '
    		    + '                 <div class="qq-thumbnail-wrapper">                                                                                  '
    		    + '                     <img class="qq-thumbnail-selector" qq-max-size="120" qq-server-scale>                                           '
    		    + '                 </div>                                                                                                              '
    		    + '                 <button type="button" class="qq-upload-cancel-selector qq-upload-cancel">X</button>                                 '
    		    + '                 <button type="button" class="qq-upload-retry-selector qq-upload-retry">                                             '
    		    + '                     <span class="qq-btn qq-retry-icon" aria-label="Retry"></span>                                                   '
    		    + '                     Retry                                                                                                           '
    		    + '                 </button>                                                                                                           '
                + '                                                                                                                                     '
    		    + '                 <div class="qq-file-info">                                                                                          '
    		    + '                     <div class="qq-file-name">                                                                                      '
    		    + '                         <span class="qq-upload-file-selector qq-upload-file"></span>                                                '
    		    + '                         <span class="qq-edit-filename-icon-selector qq-btn qq-edit-filename-icon" aria-label="Edit filename"></span>'
    		    + '                     </div>                                                                                                          '
    		    + '                     <input class="qq-edit-filename-selector qq-edit-filename" tabindex="0" type="text">                             '
    		    + '                     <span class="qq-upload-size-selector qq-upload-size"></span>                                                    '
    		    + '                     <button type="button" class="qq-btn qq-upload-delete-selector qq-upload-delete">                                '
    		    + '                         <span class="qq-btn qq-delete-icon" aria-label="Delete"></span>                                             '
    		    + '                     </button>                                                                                                       '
    		    + '                     <button type="button" class="qq-btn qq-upload-pause-selector qq-upload-pause">                                  '
    		    + '                         <span class="qq-btn qq-pause-icon" aria-label="Pause"></span>                                               '
    		    + '                     </button>                                                                                                       '
    		    + '                     <button type="button" class="qq-btn qq-upload-continue-selector qq-upload-continue">                            '
    		    + '                         <span class="qq-btn qq-continue-icon" aria-label="Continue"></span>                                         '
    		    + '                     </button>                                                                                                       '
    		    + '                 </div>                                                                                                              '
    		    + '             </li>                                                                                                                   '
    		    + '         </ul>                                                                                                                       '
                + '                                                                                                                                     '
    		    + '         <dialog class="qq-alert-dialog-selector">                                                                                   '
    		    + '             <div class="qq-dialog-message-selector"></div>                                                                          '
    		    + '             <div class="qq-dialog-buttons">                                                                                         '
    		    + '                 <button type="button" class="qq-cancel-button-selector">Close</button>                                              '
    		    + '             </div>                                                                                                                  '
    		    + '         </dialog>                                                                                                                   '
                + '                                                                                                                                     '
    		    + '         <dialog class="qq-confirm-dialog-selector">                                                                                 '
    		    + '             <div class="qq-dialog-message-selector"></div>                                                                          '
    		    + '             <div class="qq-dialog-buttons">                                                                                         '
    		    + '                 <button type="button" class="qq-cancel-button-selector">No</button>                                                 '
    		    + '                 <button type="button" class="qq-ok-button-selector">Yes</button>                                                    '
    		    + '             </div>                                                                                                                  '
    		    + '         </dialog>                                                                                                                   '
                + '                                                                                                                                     '
    		    + '         <dialog class="qq-prompt-dialog-selector">                                                                                  '
    		    + '             <div class="qq-dialog-message-selector"></div>                                                                          '
    		    + '             <input type="text">                                                                                                     '
    		    + '             <div class="qq-dialog-buttons">                                                                                         '
    		    + '                 <button type="button" class="qq-cancel-button-selector">Cancel</button>                                             '
    		    + '                 <button type="button" class="qq-ok-button-selector">Ok</button>                                                     '
    		    + '             </div>                                                                                                                  '
    		    + '         </dialog>                                                                                                                   '
    		    + '     </div>                                                                                                                          '
    		    + ' </script>                                                                                                                           '
    		    + ' <div id="uploader"></div>                                                                                                           '
    			+ '            </div>                                                                                       '
    			+ '            <div class="modal-footer">                                                                   '
    			+ '                <button type="button" class="btn btn-default" data-dismiss="modal">닫기</button>         '
    			+ '            </div>                                                                                       '
    			+ '        </div>                                                                                           '
    			+ '    </div>                                                                                               '
    			+ '</div>     	                                                                                            ';
    		$(".right_col").append(html);
    	}
    	$("#fileUploadPopupModal").on("hidden.bs.modal" , function (){
    	});
		var uploader = new qq.FineUploader({                	
		    element: document.getElementById("uploader"),
		    request : {
		    	endpoint : endpoint
		    }
	    })
    	$("#fileUploadPopupModal").modal({backdrop: 'static'});
    }
    
    /**
     * jquery 내부에서 호출 불가로 util에서 재정의
     */
    this.jsonToStringify = function (obj){
    	return JSON.stringify(obj);
    }
    
    this.sessionExpire = function (e){
    	console.error(e);
		if(e.status == 401){
			kpcUtil.customAlert("세션이 만료 되었습니다.");
	    	location.href ='/backOffice/login';                                		
		}
    }
    
    this.getCommonCodes = function (jsonData){
        $.ajax({
            url: "/api/systemMng/common/commonCodes",
            data : jsonData.param,
            type: 'GET',
            dataType : "json",
            contentType  : "application/json",
        }).done(function(data){
        	jsonData.callBack(data);
        }).fail(function(e){
        	kpcUtil.errorHandling(e);
        });      	
    }
    
    /**
     * jsonData : ,modalTitle : 모달 제목
     *            ,button  : 사용자 버튼 
     *            ,event   : body 호출 방식 
     *               - url : ajax 를 사용해서 body data를 가져온다
     *               - html : 호출 페이지에서 String 으로 전달
     *            ,url : modalType 이 "URL" 일 경우 사용
     *            ,params : modalType 이 "URL" 일 경우 사용 
     *                      queryString 형식의 parameter key1=val&key2=val2
     *            ,method : modalType 이 "URL" 일 경우 사용 
     *                    http method type
     *            ,bodyHtml : modalType 이 "URL"이 아닌경우 사용
     */
    this.openCommonPopup = function(jsonData){
    	try{
    		// 중복 실행 방지
    		$("input[type!=hidden]").not("#startDate, #endDate")[0].focus()
    	} catch(e){
    		
    	}    	

    	var popupType = jsonData.hasOwnProperty('popupType') ? jsonData.popupType : "unKnown";
    	var modalBody = "";
    	
    	
    	if (popupType == "layout") {
    		modalBody = '<div class="dynamic-modal-body modal-body form"></div>'
    	}
		else {
			modalBody = '<div class="dynamic-modal-body modal-body"></div>'
		}
    	

    	var modalSize = jsonData.hasOwnProperty('modalSize') ? jsonData.modalSize: "modal-md";
		var html = ''
			 + '<div class="modal fade" id="commonPopupModal"  role="dialog" aria-labelledby="commonPopupModalLabel">'
			 + '    <div class="modal-dialog '+modalSize+'" role="document">                                                  '
			 + '        <div class="modal-content">                                                                      '
			 + '            <div class="modal-header">                                                                   '
			 + '                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span        '
			 + '                        aria-hidden="true">&times;</span></button>                                       '
			 + '                <h4 class="modal-title" style="text-align:center;" id="commonPopupModalLabel">'+jsonData.modalTitle+'</h4>          '
			 + '            </div>                                                                                       '
			 + modalBody
			 + '            <div class="modal-footer">                                                                   ';
		if(jsonData.hasOwnProperty('button')){
			html+= jsonData.button;
		}
		html+='                <button type="button" class="dt-button btn red btn-outline closeBtn" data-dismiss="modal">닫기</button>'
		 	 + '            </div>                                                                                       '
			 + '        </div>                                                                                           '
			 + '    </div>                                                                                               '
			 + '</div>';
		$("#commonPopupModal").remove();
		$(".right_col").append(html);
    	if(jsonData.hasOwnProperty('modalType') && jsonData.modalType === "URL"){
    		kpcUtil.getAjaxContent(jsonData.URL,jsonData.params, jsonData.method, ".dynamic-modal-body");
    	}else{
    		$(".dynamic-modal-body").html(jsonData.bodyHtml);
    	}
    	if(jsonData.hasOwnProperty('buttonEvent')){
    		for(var idx in jsonData.buttonEvent){
    			$(jsonData.buttonEvent[idx].target).unbind(jsonData.buttonEvent[idx].eventType);
    			$(jsonData.buttonEvent[idx].target).on(jsonData.buttonEvent[idx].eventType ,jsonData.buttonEvent[idx].callBack);
    		}
    	}
    	$("#commonPopupModal").modal({backdrop: 'static'}).on("hidden.bs.modal",function (){
    		$(this).remove();
    	});
    }    
    
    this.bzNoCheck = function (fieldName , formName){
		if(kpcUtil.nullToBlank($(fieldName).val()) === ""){
			kpcUtil.customAlert("사업자등록번호를 입력해주세요.");
			return false;
		}
		if(!kpcUtil.checkBizID($(fieldName).val())){
			kpcUtil.customAlert("잘못된 사업자등록번호 입니다.");
			return false;
		}
        $.ajax({
            url: "/api/merchants/merchant/bznoCheck",
            data: $(formName).serialize(),
            type: 'GET',
            dataType : "json",
            contentType  : "application/json",
        }).done(function(data){
        	if(data.cnt > 0){
        		kpcUtil.customAlert("동일한 사업자번호가 존재합니다.");
        		$(fieldName).val("")
							.parent()
				            .parent()
				            .removeClass("has-error")
				            .removeClass("has-success")
		    				.find('i').each(function (){
							   $(this).removeClass("fa-warning")
							   		  .removeClass("fa-check");
		    				});
        	}else{
        		kpcUtil.customAlert("사용할 수 있는 사업자번호 입니다.");
        		
        	}
    	}).fail(function(e){
        	kpcUtil.errorHandling(e);
        });
    }
    
    this.bzNoDupCheck = function (fieldName , formName){
		if(kpcUtil.nullToBlank($(fieldName).val()) === ""){
			kpcUtil.customAlert("사업자등록번호를 입력해주세요.");
			return false;
		}
		if(!kpcUtil.checkBizID($(fieldName).val())){
			kpcUtil.customAlert("잘못된 사업자등록번호 입니다.");
			return false;
		}
        $.ajax({
            url: "/api/merchants/merchant/bznoCheck",
            data: $(formName).serialize(),
            type: 'GET',
            dataType : "json",
            contentType  : "application/json",
        }).done(function(data){
        	if(data.cnt > 0){
        		kpcUtil.customAlert("동일한 사업자번호가 존재합니다.");
        		$(fieldName).val("")
							.parent()
				            .parent()
				            .removeClass("has-error")
				            .removeClass("has-success")
		    				.find('i').each(function (){
							   $(this).removeClass("fa-warning")
							   		  .removeClass("fa-check");
		    				});
        	}
    	}).fail(function(e){
        	kpcUtil.errorHandling(e);
        });
    }    
    
    this.corpNoCheck = function (fieldName , formName){
    	if(kpcUtil.nullToBlank($(fieldName).val()) === ""){
    		kpcUtil.customAlert("법인등록번호를 입력해주세요.");
    		return false;
    	}
    	$.ajax({
    		url: "/api/merchants/merchant/corpNoCheck",
    		data: $(formName).serialize(),
    		type: 'GET',
    		dataType : "json",
    		contentType  : "application/json",
    	}).done(function(data){
			if(data.cnt > 0){
				kpcUtil.customAlert("동일한 법인등록번호가 존재합니다.");
        		$(fieldName).val("")
							.parent()
				            .parent()
				            .removeClass("has-error")
				            .removeClass("has-success")
		    				.find('i').each(function (){
							   $(this).removeClass("fa-warning")
							   		  .removeClass("fa-check");
		    				});
			}else{
				kpcUtil.customAlert("사용할 수 있는 법인등록번호 입니다.");
				
			}
		}).fail(function(e){
	    	kpcUtil.errorHandling(e);
	    });    	
    }
    
    this.openPasswordChange = function (){
    	var buttonHtml = '<button type="button" class="dt-button btn green btn-outline btnSave">수정</button>';
   		kpcUtil.openCommonPopup({
   			button : buttonHtml,
   			modalTitle : "비밀번호 변경",
   			modalSize : "custom-sm-modal-body",
   			modalType : "URL",
   			URL : "/systemMng/employees/passwordChange",
   			method : "GET",
   			buttonEvent : [
   						// 대표 거래처 수정 이벤트
   			   			{
   			   				target : ".btnSave",
   			   				eventType : "click",
   			   				callBack : function (){
   			   					if($("#passwordForm").valid() && kpcUtil.confirm("저장 하시겠습니까?") ){
   			    					$.ajax({
   			    	                    url: "/api/systemMng/employee/passwordChange",
   			    	                    data : $("#passwordForm").serializeObject(),
   			    	                    type: 'PUT',
   			    	                    dataType : "json",
   			    	                    contentType  : "application/json",
   			                        }).done(function(data){
   			                        	if(kpcUtil.successHandling("#merchantUptForm",data,false))
   			                        		$(".modal").modal('hide');
   				                    }).fail(function(e){
   				                    	kpcUtil.errorHandling(e);
   				                    });
   			   					}
   			   				}
   			   			},
   			   			{
   			   				target : ".modal",
   			   				eventType : "shown.bs.modal",
   			   				callBack : function (){
   			   					$("#beforePassword").focus();
   			   					$("#passwordForm").validate({
		   			   		        errorElement: 'span', //default input error message container
		   			   		        errorClass: 'help-block help-block-error', // default input error message class
		   			   		        rules: {
		   			   		        	beforePassword : {
		   			   		                required : true,
		   			   		                minlength : 4,
		   			   		            },
		   			   		            newPassword : {
		   			   		            	required : true,
		   			   		            	minlength : 8,
		   			   		            	passwordValidateCheck : true,
		   			   		            },
		   			   		            newPassword2 : {
		   			   		            	required : true,
		   			   		            	minlength : 8,
		   			   		            	equalTo : "#newPassword",
	   			   		            		passwordValidateCheck : true,
		   			   		            },
		   			   		        },
		   			   		        messages : {
		   			   		        	beforePassword : {
		   			   		                required : "현재 비밀번호를 입력해주세요.",
		   			   		                minlength : "4자리 이상의 비밀번호를 입력해주세요.",
		   			   		            },
	   			   		            	newPassword : {
		   			   		            	required : "새 비밀번호를 입력해주세요.",
		   			   		            	minlength : "4자리 이상의 비밀번호를 입력해주세요.",
		   			   		            	passwordValidateCheck : "1자리이상의 특수문자를 조합하여주세요."
		   			   		            },
		   			   		            newPassword2 : {
		   			   		            	required : "새 비밀번호를 입력해주세요.",
		   			   		            	minlength : "4자리 이상의 비밀번호를 입력해주세요.",
		   			   		            	equalTo : "새 비밀번호와 비밀번호 확인이 일치하지 않습니다.",
	   			   		            		passwordValidateCheck : "1자리이상의 특수문자를 조합하여주세요."
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
   			   			}
   			]
   		});
    }
    
    this.systemHistory = function (param){
    	var typeCode = param.typeCode;
    	var desc1 = param.desc1Obj;
    	var desc2 = param.desc2Obj;
    	var desc3 = param.desc3Obj;
    	var menuId = param.menuId;
		$.ajax({
			url: "/api/systemMng/common/systemHistory",
			data: JSON.stringify({
				typeCode : typeCode,
				desc1 : param.desc1,
				desc2 : param.desc2,
				desc3 : param.desc3,
				menuId : menuId,
			}),
			type: 'POST',
			dataType : "json",
			contentType  : "application/json",
		});

    }    
    
    this.openSystemHistoryConfirm = function (param){
    	var confirmMsg = param.confirmMsg;
    	var confirmTitle = param.confirmTitle;
    	var typeCode = param.typeCode;
    	var desc1 = param.desc1Obj;
    	var desc2 = param.desc2Obj;
    	var desc3 = param.desc3Obj;
    	var menuId = param.menuId;
    	var alertMsg = param.alertMsg;
    	var targetForm = param.targetForm;
    	var beforeAjaxParam = param.beforeAjaxParam;
    	var placeHolder = (param.placeHolder!="")? param.placeHolder : "";
    	var afterCAllBack = param.afterCAllBack;
   		var bodyHtml = '<div class="row" style="margin-top:10px;">'
	        + '<div class="col-md-12 col-sm-12 col-xs-12">'
	        + '    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
	        + '        <label class="control-label col-md-12 col-sm-12 col-xs-12"><b>'+confirmMsg+'</b></label>'
	        + '     </div>'
	        + '</div>'
            + '<div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 form-group">'
            + '    <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'
	        + '        <input type="text" id="desc2" name="desc2" class="form-control col-md-7 col-xs-12" placeholder="'+placeHolder+'" maxlength="20">'
            + '    </div>'
            + '</div>'
            + '</div>'
	         ;
   		var buttonHtml = '<button type="button" class="dt-button btn green btn-outline btnSave">확인</button>';
   		kpcUtil.openCommonPopup({
   			modalTitle : confirmTitle,
   			bodyHtml : bodyHtml,
   			button : buttonHtml,
   			modalSize : "custom-sm-modal-body",
   			buttonEvent : [{
   				target : ".btnSave",
   				eventType : "click",
   				callBack : function (){
   					if($(desc2).val().trim().length < 1){
   						kpcUtil.customAlert(confirmTitle + "사유를 입력해주세요.");
   						return false;
   					}
   					if(menuId=="CPN-0001"){
   						//.desc2 = $(desc2).val();
   						var jsonData = JSON.parse(beforeAjaxParam.data);
   						jsonData["desc2"] =  ($(desc2).val()!="")? $(desc2).val() : "";
   						beforeAjaxParam.data = JSON.stringify(jsonData);
   					}
   					
   					$.ajax(beforeAjaxParam).done(function (resultData){
   						console.log(resultData);
   						if(kpcUtil.kpcApiSuccessHandling(targetForm, resultData, false)){
   							kpcUtil.customAlert(alertMsg);
   							afterCAllBack();
   							$(".modal").modal('hide');
   						}
   						
   						var desc1Val = (kpcUtil.nullToBlank($(desc1).val())=="")? desc1 : kpcUtil.nullToBlank($(desc1).val());
   						var desc2Val = (kpcUtil.nullToBlank($(desc2).val())=="")? desc2 : kpcUtil.nullToBlank($(desc2).val());
   						var desc3Val = (kpcUtil.nullToBlank($(desc3).val())=="")? desc3 : kpcUtil.nullToBlank($(desc3).val());
   						
   						$.ajax({
   							url: "/api/systemMng/common/systemHistory",
   							data: JSON.stringify({
   								typeCode : typeCode,
   								desc1 : desc1Val,
   								desc2 : desc2Val,
   								desc3 : desc3Val,
   								menuId : menuId
   							}),
   							type: 'POST',
   							dataType : "json",
   							contentType  : "application/json",
   							async : true,
   						});
   					
   					}).fail(function (e){
   						kpcUtil.errorHandling(e);
   					});
				}
   			}]
   		});    	
    }
    
    this.openSystemHistoryModal = function (param){
		var bodyHtml = ''
 	         + '<table id="historyTable" class="table table-striped table-bordered" >'
           + '    <thead>'
           + '        <tr>'
           + '            <th>번호</th>'
           + '            <th>변경일</th>'
           + '            <th>변경시간</th>'
           + '            <th>처리구분</th>'
           + '            <th>변경내용</th>'
           + '            <th>사유</th>'
           + '            <th>수정자</th>'
           + '        </tr>'
           + '    </thead>'
           + '    <tbody>'
           + '    </tbody>'
		        + '</table>'
           ;
  		kpcUtil.openCommonPopup({
  			modalTitle : "제한이력 조회",
  			bodyHtml : bodyHtml,
  			modalSize : "custom-md-modal-body",
  			buttonEvent : [
  			  // 모달 이벤트
  			  {
  			  	target : ".modal",
  			  	eventType : "shown.bs.modal",
  			  	callBack : function (){
  		            $('#historyTable').dataTable({
		                    "bProcessing": true,
  		                    "bServerSide": true,
  		                    "deferRender": true,
  		                    "ajax": {
  		                        "url": "/api/systemMng/common/systemHistory",
  		                        "async" : "true",
  		                        "data": function (parameter) {
  		                            parameter.menuId = param.menuId;
  		                            parameter.desc1 = $(param.desc1).val();
  		                        },
  		                        "error" : function (e){kpcUtil.sessionExpire(e);}
  		                    },
  		                    "ordering": false,
  		                    columns: [
                                {
                                  	data : "regDt" , 
  	                                defaultContent: "",
  	                                width : 90,
  	                                className: "column-align-center" ,  	                                
  	                                render : function (data, type , full , meta){
  	                                	return kpcUtil.setDateFormat(full.regDt, "YYYY-MM-DD");
  	                                }
                                }, // 등록일  		                        
                                {
                                  	data : "regDt" , 
  	                                defaultContent: "", 
  	                                width : 90,
  	                                className: "column-align-center" ,  	                                
  	                                render : function (data, type , full , meta){
  	                                	return kpcUtil.setDateFormat(full.regDt , "HH:mm:ss");
  	                                }
                                }, // 등록시간
                                {data: "desc3", defaultContent: "",  className: "column-align-center"}, // 구분
  		                        {data: "typeName", defaultContent: "",  className: "column-align-center"}, // 구분  		                        
  		                        {data: "desc2", defaultContent: "",  className: "column-align-center"}, // 사유
  		                        {data: "regId", defaultContent: "",  className: "column-align-center"}, // 등록자
  		                    ],
  		                  "order" : [[1,'desc']],
  		                  "paging" : true,
  		                  "lengthMenu": [[5, 10, 20, 50, 200], [5, 10, 20, 50, 200]],
                          "pageLength": 5,
                          "dom": "<'row' <'col-md-12 col-sm-12'l>><'table-scrollable'tr><'row'<'col-md-6 col-sm-6'i><'col-md-6 col-sm-6'p>>",
  		                    responsive: true,
  		                    "language": {
  		                        "aria": {
  		                            "sortAscending": ": activate to sort column ascending",
  		                            "sortDescending": ": activate to sort column descending"
  		                        },
  		                        "info":"Total Record: _TOTAL_ Page : _START_ / _PAGES_ ",
  		                        "emptyTable": "조회된 자료가 없습니다.",
  		                        "infoEmpty": "조회된 자료가 없습니다.",
  		                        "lengthMenu": "_MENU_",
  		                        "zeroRecords": "조회된 자료가 없습니다.",
  		                    },
		               });
  			  		}
  			  }]
  		});    	
    }
    

    this.openCardRestrictHistoryModal = function (param){
		var bodyHtml = ''
 	         + '<table id="historyTable" class="table table-striped table-bordered" >'
           + '    <thead>'
           + '        <tr>'
           + '            <th>번호</th>'
           + '            <th>변경일</th>'
           + '            <th>변경시간</th>'
           + '            <th>처리구분</th>'
           + '            <th>변경내용</th>'
           + '            <th>사유</th>'
           + '            <th>수정자</th>'
           + '        </tr>'
           + '    </thead>'
           + '    <tbody>'
           + '    </tbody>'
		        + '</table>'
           ;
  		kpcUtil.openCommonPopup({
  			modalTitle : "제한이력 조회",
  			bodyHtml : bodyHtml,
  			modalSize : "custom-md-modal-body",
  			buttonEvent : [
  			  // 모달 이벤트
  			  {
  			  	target : ".modal",
  			  	eventType : "shown.bs.modal",
  			  	callBack : function (){
  		            $('#historyTable').dataTable({
		                    "bProcessing": true,
  		                    "bServerSide": true,
  		                    "deferRender": true,
  		                    "ajax": {
  		                        "url": "/api/card/restrictHistory",
  		                        "async" : "true",
  		                        "data": function (parameter) {
  		                            parameter.giftNo = param.giftNo;  		                        
  		                        },
  		                        "error" : function (e){kpcUtil.sessionExpire(e);}
  		                    },
  		                    "ordering": false,
  		                    columns: [
  		                    	{data : "rnum",  defaultContent: "",  className: "column-align-center"},
                                {
                                  	data : "createDt" , 
  	                                defaultContent: "",
  	                                width : 90,
  	                                className: "column-align-center" ,  	                                
  	                                render : function (data, type , full , meta){
  	                                	return kpcUtil.setDateFormat(full.createDt, "YYYY-MM-DD");
  	                                }
                                }, // 등록일  		                        
                                {
                                  	data : "createDt" , 
  	                                defaultContent: "", 
  	                                width : 90,
  	                                className: "column-align-center" ,  	                                
  	                                render : function (data, type , full , meta){
  	                                	return kpcUtil.setDateFormat(full.createDt , "HH:mm:ss");
  	                                }
                                }, // 등록시간
                                {data: "rtype", defaultContent: "",  className: "column-align-center",
                                	render : function(data, type , full , meta){
                                		if(full.rtype=="ON"){
                                			return "POP";
                                		}else{
                                			return full.rtype;
                                		}
                                	}
                                }, // 구분
  		                        {
                                	data: "useFlag", 
                                	defaultContent: "",
                                	className: "column-align-center",
                                	render : function(data, type, full, meta){
                                		var useFlag = (full.useFlag=="N")? "사용해제" : "사용제한";
                                		return useFlag;
                                	}
                                		
                                }, // 구분  		                        
  		                        {data: "reqDesc", defaultContent: "",  className: "column-align-center"}, // 사유
  		                        {data: "regId", defaultContent: "",  className: "column-align-center"}, // 등록자
  		                    ],
  		                  "order" : [[1,'desc']],
  		                  "paging" : true,
  		                  "lengthMenu": [[10, 20, 50], [10, 20, 50]],
                          "pageLength": 10,
                          "dom": "<'row' <'col-md-12 col-sm-12'l>><'table-scrollable'tr><'row'<'col-md-6 col-sm-6'i><'col-md-6 col-sm-6'p>>",
  		                    responsive: true,
  		                    "language": {
  		                        "aria": {
  		                            "sortAscending": ": activate to sort column ascending",
  		                            "sortDescending": ": activate to sort column descending"
  		                        },
  		                        "info":"Total Record: _TOTAL_ Page : _START_ / _PAGES_ ",
  		                        "emptyTable": "조회된 자료가 없습니다.",
  		                        "infoEmpty": "조회된 자료가 없습니다.",
  		                        "lengthMenu": "_MENU_",
  		                        "zeroRecords": "조회된 자료가 없습니다.",
  		                    },
		               });
  			  		}
  			  }]
  		});    	
    }
    
    this.serachFormEvent = function (obj){
    	if(typeof obj.selects !== "undefined"){
    		$(obj.selects).change(function (){
    			obj.callback();
    		});
    	}
    	if(typeof obj.inputs !== "undefined"){
	        $(obj.inputs).keyup(function(e) {
	            if (e.keyCode == 13) {
	            	obj.callback();
	            }
	        });
    	}
    }
    
    this.setFormTextFieldFormat = function (obj){
        $(obj.target).find("input").each(function (){
        	if($(this).attr("isTel")){
        		$(this).keyup(function (e){
        			var key = e.which;
        			switch(key){
        				case 16 : // shift
        					break;
        				case 17 : // ctrl
        					break;
        				case 35 : // home
        					break;
        				case 36 : // end
        					break;
        				case 38 : // up
        					break;
        				case 37 : // left
        					break;
        				case 39 : // right
        					break;
        				case 40 : // down
        					break;
        				case 46 : // down
        					break;
        				case 65 : // a
        					break;
        				default:
        					$(this).val(kpcUtil.setTelFormat($(this).val()));
        			}
        			
        		});
        	}
        	if($(this).attr("isBzno")){
        		$(this).keyup(function (e){
        			var key = e.which;
        			switch(key){
        				case 16 : // shift
        					break;
        				case 17 : // ctrl
        					break;
        				case 35 : // home
        					break;
        				case 36 : // end
        					break;
        				case 38 : // up
        					break;
        				case 37 : // left
        					break;
        				case 39 : // right
        					break;
        				case 40 : // down
        					break;
        				case 46 : // down
        					break;
        				case 65 : // a
        					break;
        				default:
        					$(this).val(kpcUtil.setBznoFormat($(this).val()));
        			}        			
        		});
        	}   
        	if($(this).attr("delHyphen")){
        		$(this).keyup(function (e){
        			var key = e.which;
        			switch(key){
        				case 16 : // shift
        					break;
        				case 17 : // ctrl
        					break;
        				case 35 : // home
        					break;
        				case 36 : // end
        					break;
        				case 38 : // up
        					break;
        				case 37 : // left
        					break;
        				case 39 : // right
        					break;
        				case 40 : // down
        					break;
        				case 46 : // down
        					break;
        				case 65 : // a
        					break;
        				default:
        					$(this).val(kpcUtil.replaceHyphen($(this).val()));
        			}        			
        		});
        	}          	
        });    	
    }
    
    /**
     * 두날짜의 차이 일수를 return
     * param : startDate=yyyy-mm-dd ,endDate=yyyy-mm-dd
     *         형식의 날짜를 입력
     *         
     */
    this.getDiffDays = function(startDate,endDate){
    	try{
    		var splitStartDate = startDate.split('-');
    		var splitEndDate= endDate.split('-');    	
    		var sDate = new Date(parseInt(splitStartDate[0]) , parseInt(splitStartDate[1]) -1 , parseInt(splitStartDate[2]));
    		var eDate = new Date(parseInt(splitEndDate[0]) , parseInt(splitEndDate[1]) -1 , parseInt(splitEndDate[2]));
    		return Math.floor((eDate.getTime() - sDate.getTime())/(1000 *60*60*24));    	
    	}catch(e){
    		return 0;
    	}
    }

};

/**
 * submit 방지용
 * @returns
 */
function nothing(){
	return;
}