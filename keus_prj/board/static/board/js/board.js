/*게시판 내용 출력 */
function toggleContent(item) {
    var content = item.nextElementSibling;
    content.style.display = (content.style.display === 'none' || content.style.display === '') ? 'block' : 'none';
}

/* 게시판 게시글 삭제 */
function confirmDelete(postId) {
var result = confirm('게시글을 삭제하시겠습니까?');

    if (result) {
        // 동적으로 CSRF 토큰 획득
        var csrf_token = $("input[name='csrfmiddlewaretoken']").val();
        let param = {"postId" : postId}

        // 확인을 눌렀을 때, 서버로 삭제 요청을 보냄
        $.ajax({
            type: 'POST',

            url: '/board/post/delete/',  // URL 수정
            //url: '/board/post/'+postId+'/delete/',  // URL 수정
            data : JSON.stringify(param),
            headers: {
                'X-CSRFTOKEN': csrf_token,  // CSRF 토큰을 헤더에 추가
            },
            success: function (data) {
                alert(data.message);  // 서버로부터의 응답 메시지를 alert으로 표시
                window.location.href = '/board/';
                //삭제 이후의 게시글 목록으로 페이지 갱신
                //updateBoardList(data.boards);
            },
            error: function (e) {
                alert(e);
                alert('글 작성자만 삭제할 수 있습니다.');
            }
        });
    }
    else {
        return false;
    }

}
/* 20231201 하승우 추가 */
function confirmComment(postId) {
    // 입력 필드에서 값 가져오기
    var content = $('#contentInput').val();

    // 댓글 데이터 생성
    var commentData = {
        'content': content,
    };

    var result = confirm('댓글을 작성하시겠습니까?');

    if (result) {
        var csrf_token = $("input[name='csrfmiddlewaretoken']").val();

        // AJAX를 사용하여 서버로 댓글 데이터 전송
        $.ajax({
            type: 'POST',
            url: 'new_comment/',  // postId를 포함한 URL 설정
            headers: {
                'X-CSRFToken':  csrf_token,
            },
            data: commentData,
            success: function(response) {
                // 성공적으로 댓글을 작성한 경우 해당 페이지의 특정 부분을 업데이트합니다.
                // 예를 들어, 댓글 목록이 표시되는 div를 업데이트하는 코드를 작성할 수 있습니다.
                $('#commentList').load(location.href + ' #commentList');
            },
            error: function(error) {
                alert('댓글 작성에 실패했습니다.');
            }
        });
    }
}

// 게시글 목록을 갱신하는 함수
function updateBoardList(boards) {
    console.log("Received Boards:", boards);
    var boardList = $('.board-list');
    boardList.empty();

    // 헤더 추가
    boardList.append('<ul class="subject">' +
        '<li id="bnum">번호</li>' +
        '<li id="btitle" style="text-align: center;">제목</li>' +
        '<li id="bid">작성자</li>' +
        '<li id="bdate">작성일</li>' +
        '</ul>');

    for (var i = 0; i < boards.length; i++) {
        var board = boards[i];
        var listItem = '<ul onclick="toggleContent(this)">' +
            '<li id="bnum">' + (i + 1) + '</li>' +  // 수정된 부분: 각 게시글의 index를 사용
            '<li id="btitle">' + board.title + '</li>' +
            '<li id="bid">' + board.member__username + '</li>' +
            '<li id="bdate">' + board.created_at + '</li>' +
            '</ul>' +
            '<div class="content">' +
            '<p>' + board.contents + '</p>' +
            '<button type="button" onclick="confirmDelete(\'' + board.id + '\')">삭제</button>' +
            '</div>';
        boardList.append(listItem);
    }
}

