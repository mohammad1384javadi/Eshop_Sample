function sendArticleComment(articleId) {
    var comment = $('#commentText').val();
    var parentId = $('#parent_id').val();
    console.log(parentId);
    $.get('/articles/add_article_comment', {
        article_comment: comment,
        article_id: articleId,
        parent_id : parentId
    }).then(res => {
        $('#comment-area').html(res);
        $('#commentText').val('');
        $('#parent_id').val('');

        if (parentId !== null && parentId !== '') {
            document.getElementById('single_comment_box_' + parentId).scrollIntoView({behavior: "smooth"});
        }
        else{
            document.getElementById('comment-area').scrollIntoView({behavior: "smooth"});
        }
    });
}

function fillParentId(parentId) {
    $('#parent_id').val(parentId);
    document.getElementById('comment-form').scrollIntoView({behavior: "smooth"});
}



function fillProducts(){
    const filterPrice = $('#sl2').val();
    const start_price = filterPrice.split(',')[0];
    const end_price = filterPrice.split(',')[1];
    $('#start_price').val(start_price);
    $('#end_price').val(end_price);
    $('#filter_form').submit();
}

function fillPage(page){
    $('#page').val(page);
    $('#filter_form').submit();
}

function showLargeImage(imageSrc){
    $('#main_image').prop('src', imageSrc);
    $('#show_large_image_modal').attr('href', imageSrc);
}

function addProductToOrder(productId){
    const productCount = $('#product_count').val();
    $.get('/order/add_to_order?product_id=' + productId + '&count=' + productCount).then(res => {
        Swal.fire({
            title: 'اعلان',
            text: res.text,
            icon: res.icon,
            showCancelButton: false,
            confirmButtonColor: '#3085d6',
            confirmButtonText: res.confirm_button_text
        }).then(result => {
            if (result.isConfirmed && res.status === 'not_auth'){
                // if (res.status === 'not_auth'){
                //     window.location.href = '/login';
                // }
                window.location.href = '/login'
            }
        });
    })
}

function removeOrderDetail(detailId){
    $.get('/user/remove_order_detail?detail_id=' + detailId).then(res => {
        if (res.status === 'success'){
            $('#order_detail_content').html(res.body);
        }
    });
}


function changeOrderDetailCount(detailId, state){
    $.get('/user/change_order_detail?detail_id=' + detailId + '&state=' + state).then( res => {
        if (res.status === 'success'){
            $('#order_detail_content').html(res.body);
        }
    });
}