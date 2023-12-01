// 아이디와 비밀번호 찾기위한 handleFindResponse함수
// 비밀번호 찾기 -> 임시비밀번호 발급 으로 변경 ( temporary password )
function handleFindResponse(response) {
    if ('error' in response) {
        alert('에러 발생: ' + response.error);
    } else {
        if ('username' in response) {
            alert('아이디는: ' + response.username + '입니다.');
        } else if ('temp_password' in response) {
            alert('임시 비밀번호는: '  + response.temp_password +  '입니다. 보안을 위해 빠르게 비밀번호를 변경해주시기 바랍니다.');
        } else {
            alert('해당 내용을 찾을 수 없습니다. 다시 입력해주세요.');
        }
    }
}

$(document).ready(function () {
    $('.find-form').submit(function (event) {
        event.preventDefault();

        var formData = $(this).serialize();
        var actionUrl = $(this).attr('action');

        $.ajax({
            url: actionUrl,
            method: 'GET',
            data: formData,
            success: function (response) {
            // 성공적으로 응답을 받으면 handleFindResponse 함수 호출
                handleFindResponse(response);
            },
            error: function (error) {
                console.error('에러 발생:', error);
            }
        });
    });
});

