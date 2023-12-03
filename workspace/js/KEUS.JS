findform = document.getElementById("join-form")
// 아이디 중복체크를 위한 전역변수 설정

// 아이디 중복체크
function ID_check() {
    // 입력된 아이디 가져오기
    var username = $("#id").val().trim();

    // 아이디가 비어 있는지 확인
    if (username.length === 0) {
        alert("아이디를 입력해주세요.");
        $("#id").focus();
        return;
    }

    // 서버에 아이디를 확인하기 위한 AJAX 요청
    $.ajax({
        url: '/member/check_username/',
        method: 'POST',
        data: {
            'username': username,
            'csrfmiddlewaretoken': findform.csrfmiddlewaretoken.value,
        },
        success: function (response) {

            if (response.status === 'success') {
                alert("사용가능한 아이디입니다.");
            } else if (response.status === 'error') {
                alert("이미 존재하는 아이디입니다.");
            }
        },
        error: function (error) {
            console.error('에러 발생:', error);
        }
    });

    event.preventDefault();
}

// 이용약관 모두체크
function selectAll(selectAll)  {
    const checkboxes
         = document.getElementsByName('check');

    checkboxes.forEach((checkbox) => {
      checkbox.checked = selectAll.checked;
    })
}

function validate() {


    // 아이디
    if ($("#id").val().trim().length === 0) {
        alert("아이디를 입력해주세요.");
        $("#id").focus();
        return false;
    }

    var username = $("#id").val().trim();
    var idRegex = /^[a-zA-Z0-9_]{4,20}$/;

    if (!idRegex.test(username)) {
        alert("아이디는 4~20자리의 영문, 숫자, 특수문자 '_'만 사용 가능합니다.");
        return false;
    }

    // 비밀번호
    if ($("#pw").val().trim().length === 0) {
        alert("비밀번호를 입력해주세요.");
        $("#pw").focus();
        return false;
    }

    // 비밀번호 형식체크
    var password = $("#pw").val().trim();
    var passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,20}$/;

    if (!passwordRegex.test(password)) {
        alert("비밀번호는 8~20자리의 영문, 숫자, 특수문자를 모두 포함해야 합니다.");
        return false;
    }

    // 비밀번호 확인
    if ($("#pwok").val().trim().length === 0) {
        alert("비밀번호 확인을 입력해주세요.");
        $("#pwok").focus();
        return false;
    }
    // 비밀번호 일치 확인
    if ($("#pw").val() !== $("#pwok").val()) {
        alert("비밀번호가 일치하지 않습니다.");
        $("#pw").focus();
        return false;
    }

    // 이메일
    if ($("#email").val().trim().length === 0) {
        alert("이메일을 입력해주세요.");
        $("#email").focus();
        return false;
    }

    // 이메일 형식체크
    var email = $("#email").val().trim();
    var emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;

    if (!emailRegex.test(email)) {
        alert("이메일 형식에 맞게 입력해주세요.");
        $("#email").focus();
        return false;
    }
    // 이메일 중복 체크
    var email = $("#email").val().trim();
    var emailCheckPromise = new Promise(function (resolve, reject) {
        $.ajax({
            url: '/member/check_email/',
            method: 'POST',
            data: {
                'email': email,
                'csrfmiddlewaretoken': findform.csrfmiddlewaretoken.value,
            },
            success: function (response) {
                if (response.status === 'error') {
                    alert("이미 등록된 이메일입니다.");
                    $("#email").focus();
                    reject("이메일 중복 에러");
                } else {
                    resolve("이메일 중복 확인 통과");
                }
            },
            error: function (error) {
                console.error('에러 발생:', error);
                reject("이메일 중복 확인 실패");
            }
        });
    });

    // 전화번호
    if ($("#phone").val().trim().length === 0) {
        alert("전화번호를 입력해주세요.");
        $("#phone").focus();
        return false;
    }

    // 전화번호 형식체크
    var phone = $("#phone").val().trim();
    var phoneRegex = /^[0-9]+$/;

    if (!phoneRegex.test(phone)) {
        alert("숫자만 입력해주세요.");
        $("#phone").focus();
        return false;
    }

    // 전화번호 중복 체크
    var phone = $("#phone").val().trim();
    var phoneCheckPromise = new Promise(function (resolve, reject) {
        $.ajax({
            url: '/member/check_tell/',
            method: 'POST',
            data: {
                'Tell': phone,
                'csrfmiddlewaretoken': findform.csrfmiddlewaretoken.value,
            },
            success: function (response) {
                if (response.status === 'error') {
                    alert("이미 등록된 전화번호입니다.");
                    $("#phone").focus();
                    reject("전화번호 중복 에러");
                } else {
                    resolve("전화번호 중복 확인 통과");
                }
            },
            error: function (error) {
                console.error('에러 발생:', error);
                reject("전화번호 중복 확인 실패");
            }
        });
    });
    // 약관 동의
    if (!$("#agree_1").prop("checked") || !$("#agree_2").prop("checked")) {
        alert("약관에 동의해주세요.");
        return false;
    }



Promise.all([emailCheckPromise, phoneCheckPromise])
    .then(function (results) {
        // 두 중복 확인(이메일.전화번호)이 모두 통과했을 때만 회원가입 진행
        alert("회원가입이 완료되었습니다.");
        //return true;
        // 회원가입이 성공할 경우에 join form 제출
        document.getElementById("join-form").submit();
    })
    .catch(function (error) {
        // 적어도 하나의 중복 확인이 실패했을 때는 회원가입 진행하지 않음
        return false;

    });
     event.preventDefault();
}

/*게시판 내용 출력 */
function toggleContent(item) {
    var content = item.nextElementSibling;
    content.style.display = (content.style.display === 'none' || content.style.display === '') ? 'block' : 'none';
}