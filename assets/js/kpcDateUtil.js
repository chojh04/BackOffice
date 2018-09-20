
/**
 * 두 날짜 차이 비교.
 * 더 자세한 내용은 momentjs guide 참고 바랍니다. -민욱
 * @param startDate 시작일
 * @param endDate 종료일
 * @param diffType (ex. "years" "months" "weeks" "days" "hours, "minutes", "seconds")
 * @param range 비교 할 기간
 * @returns
 */
function dateRangeDiff(startDate, endDate, diffType, range) {

	var startDate = moment(startDate);
	var endDate = moment(endDate);
	
	if (endDate.diff(startDate, diffType) > range) {
		return true;
	}
	else {
		return false;
	}
}