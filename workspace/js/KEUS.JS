
// 아이디 중복체크
function ID_check() {
    alert("사용가능한 아이디입니다.");
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

    // 약관 동의
    if (!$("#agree_1").prop("checked") || !$("#agree_2").prop("checked")) {
        alert("약관에 동의해주세요.");
        return false;
    }

    alert("회원가입이 완료되었습니다.");
    location.href = 'login.html';
    return true;
}

