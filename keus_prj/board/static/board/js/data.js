document.getElementById('searchButton').addEventListener('click', function () {
    var selectedRegions = getSelectedValues('check', '지역 선택');
    var selectedYears = getSelectedValues('check', '연도 선택');

    // 예측 시작 시 팝업 표시
    alert('데이터 조회를 시작합니다. 확인버튼을 눌러주세요');

    // 서버로 비동기 요청 보내기
    fetch('predict/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ regions: selectedRegions, years: selectedYears })
    })
    .then(response => response.json())
    .then(data => {
        // 작업이 완료되면 완료 메시지 표시
        alert(data.message);
    });
});

function getSelectedValues(className, headerText) {
    var selectedValues = [];
    var checkboxes = document.querySelectorAll('.' + className + ' input[type="checkbox"]:checked');

    if (checkboxes.length === 0) {
        alert(headerText + '을(를) 선택하세요.');
    } else {
        checkboxes.forEach(function (checkbox) {
            selectedValues.push(checkbox.value);
        });
    }

    return selectedValues;
}


document.getElementById('searchButton_ele').addEventListener('click', function () {
    var selectedRegions = getSelectedValues('check', '지역 선택');
    var selectedYears = getSelectedValues('check', '연도 선택');

    // 예측 시작 시 팝업 표시
    alert('데이터 조회를 시작합니다. 확인버튼을 눌러주세요');

    // 서버로 비동기 요청 보내기
    fetch('predict_ele/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ regions: selectedRegions, years: selectedYears })
    })
    .then(response => response.json())
    .then(data => {
        // 작업이 완료되면 완료 메시지 표시
        alert(data.message);
    });
});