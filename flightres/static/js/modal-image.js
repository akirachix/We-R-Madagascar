
$(document).ready(function () {

  image_urls_unstructured = image_url_objects.replace(/&quot;/g, '"');
  image_urls = JSON.parse(image_urls_unstructured)

  var imageBtn = document.getElementsByClassName('expandImage')
  // console.log(imageBtn);

  for (var i = 0; i < imageBtn.length; i++) {
    imageBtn[i].addEventListener('click', function (e) {
      console.log('clicked');
      object_id = e.target.id.split('_')[1]
      for (j = 0; j < image_urls.length; j++) {
        if (object_id == image_urls[j].uav_uid) {
          createModal(image_urls[j])
          // console.log(object_id, image_urls[j].uav_uid);
        }
      }
    })
  }

  function createModal(data) {
    var html1 = `
    <div class="mySlides" style="display: block;">
      <img src="`+ data.image_url + `"
        style="width:100%">
    </div>
    `
    console.log(html1, "shown");
    openModal()
    document.getElementById("openFSImage").innerHTML = html1;
  }
});

function openModal() {
  //   document.getElementById("myModal").style.display = "block";
  console.log("Open Modal Clicked");
  document.getElementById("myModal").classList.add("open");
}

function closeModal() {
  //   document.getElementById("myModal").style.display = "none";
  document.getElementById("myModal").classList.remove("open");
}

// var slideIndex = 1;
// showSlides(slideIndex);

// function plusSlides(n) {
//   showSlides(slideIndex += n);
// }

// function currentSlide(n) {
//   showSlides(slideIndex = n);
// }

// function showSlides(n) {
//   var i;
//   var slides = document.getElementsByClassName("mySlides");
//   if (n > slides.length) { slideIndex = 1 }
//   if (n < 1) { slideIndex = slides.length }
//   for (i = 0; i < slides.length; i++) {
//     slides[i].style.display = "none";
//   }
//   slides[slideIndex - 1].style.display = "block";
// }