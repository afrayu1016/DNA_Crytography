<?php session_start(); ?>
<!DOCTYPE html>
<html lang="en">

<head>

     <meta charset="UTF-8">
     <meta http-equiv="X-UA-Compatible" content="IE=Edge">
     <meta name="description" content="">
     <meta name="keywords" content="">
     <meta name="author" content="">
     <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">

     <title>DNA Crytography</title>

     <link rel="stylesheet" href="css/bootstrap.min.css">
     <link rel="stylesheet" href="css/font-awesome.min.css">

     <!-- Main css -->
     <link rel="stylesheet" href="css/style.css">
     <link href="https://fonts.googleapis.com/css?family=Lora|Merriweather:300,400" rel="stylesheet">

</head>

<body>

     <!-- PRE LOADER -->

     <div class="preloader">
          <div class="sk-spinner sk-spinner-wordpress">
               <span class="sk-inner-circle"></span>
          </div>
     </div>

     <!-- Navigation section  -->

     <div class="navbar navbar-default navbar-static-top" role="navigation">
          <div class="container">

               <div class="navbar-header">
                    <button class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                         <span class="icon icon-bar"></span>
                         <span class="icon icon-bar"></span>
                         <span class="icon icon-bar"></span>
                    </button>
                    <a href="index.html" class="navbar-brand">DNA Crytography</a>
               </div>

          </div>
     </div>

     <!-- Home Section -->

     <section id="home" class="main-home parallax-section">
          <div class="overlay"></div>
          <div id="particles-js"></div>
          <div class="container">
               <div class="row">

                    <div class="col-md-12 col-sm-12">
                         <h1>Hi! This is DNA Crytography.</h1>
                         <h4>This website uses DNA crytography to encrypt and decrypt the images and text.</h4>
                         <h4>Here, you can get any cipher image and text you want. Just try it!!</h4>
                    </div>

               </div>
          </div>
     </section>

     <!-- Blog Section -->

     <section id="blog">
          <div class="container">
               <div class="row">

                    <div class="col-md-offset-1 col-md-10 col-sm-12">
                         <div class="blog-post-thumb">
                              <!-- <div class="blog-post-image">
                              <a href="single-post.html">
                                   <img src="images/blog-image1.jpg" class="img-responsive" alt="Blog Image">
                              </a>
                         </div> -->
                              <div class="blog-post-title">
                                   <center>
                                        <h2>Encrypt your images.</h2>
                                   </center>
                              </div>

                              </br>
                              </br>

                              <form action="upload.php" enctype="multipart/form-data" method="post">
                                   <div class="text_wrap">
                                        <div class="left">
                                             <center>
                                                  <p>Upload your image on right hand side.</p>

                                                  <label for="file-upload" class="custom-file-upload">Choose
                                                       File</label>
                                                  <input id="file-upload" type="file" name="file" />
                                                  <input type="submit" value="Upload" name="submit"
                                                       class="btn btn-default"> <br />
                                             </center>

                                        </div>
                                        <div class="right">
                                             <center>
                                                  <p>Click encrypted picture to download.</p>
                                             </center>


                                        </div>
                                   </div>
                              </form>

                              <div class="blog-post-des">
                                   <center><input type="submit" value="Encrypted Image" name="encrypt_img"
                                             class="btn btn-default"></center>
                              </div>
                         </div>

                         <div class="blog-post-thumb">
                              <!-- <div class="blog-post-image">
                              <a href="single-post.html">
                                   <img src="images/blog-image1.jpg" class="img-responsive" alt="Blog Image">
                              </a>
                         </div> -->
                              <div class="blog-post-title">
                                   <center>
                                        <h2>Decrypt your images.</h2>
                                   </center>
                              </div>

                              </br>
                              </br>

                              <form action="de_upload.php" enctype="multipart/form-data" method="post">
                                   <div class="img_wrap">
                                        <div class="left">
                                             <center>
                                                  <p>Upload your image on right hand side.</p>

                                                  <label for="de_file" class="custom-file-upload">Choose File</label>
                                                  <input id="de_file" type="file" name="de_file" />
                                                  <input type="submit" value="Upload" name="de_submit"
                                                       class="btn btn-default"> <br />
                                             </center>

                                        </div>
                                        <div class="right">
                                             <center>
                                                  <p>Click decrypted picture to download.</p>
                                             </center>


                                        </div>
                                   </div>
                              </form>
                              <div class="blog-post-des">
                                   <center><input type="submit" value="Decrypted Image" name="decrypt_img"
                                             class="btn btn-default"></center>
                              </div>

                         </div>



                         <div class="blog-post-thumb">
                              <div class="blog-comment-form">
                                   <div class="text_wrap">
                                        <div class="left">

                                             <center>
                                                  <h3>Plain text</h3>
                                             </center>
                                             <?php $_SESSION['plain_text'] = $_POST['plain_message']; ?>

                                             <form action="text_encrypt.php" method="post">



                                                  <textarea name="plain_message" rows="5" class="form-control"
                                                       id="message" placeholder="Plain Text" message="message"
                                                       required="required"><?php
                                                       // session_start();
                                                       if (isset($_POST['text_submit'])) {
                                                            // unset($_SESSION['plain_text']);
                                                       
                                                            $_SESSION['plain_text'] = $_POST['plain_message'];
                                                            $plaintext = $_POST['plain_message'];
                                                            // echo $plaintext;
                                                            $pythonScriptCall = 'python dna_get.py ' . $plaintext;
                                                            $pythonScriptResult = '';

                                                            exec($pythonScriptCall, $pythonScriptResult);
                                                            if ($pythonScriptResult == '') {
                                                                 echo 'Error';
                                                            }
                                                       }

                                                       if ($_SESSION['plain_text'] != '') {
                                                            echo $_SESSION['plain_text'];
                                                       }
                                                       ?></textarea>

                                        </div>
                                        <div class="center">

                                        </div>
                                        <div class="right">

                                             <center>
                                                  <h3>Cipher text</h3>
                                             </center>
                                             <textarea name="message" rows="5" class="form-control" id="message"
                                                  placeholder="Cipher Text" message="message"><?php
                                                  if (isset($_POST['text_submit'])) {
                                                       $file_content = file_get_contents('./cipher_text.txt', FILE_USE_INCLUDE_PATH);
                                                       echo $file_content;
                                                  }
                                                  ?></textarea>


                                        </div>
                                   </div>
                                   <div class="blog-post-des">
                                        <center><input name="text_submit" type="submit" class="btn btn-defaultl"
                                                  id="submit" value="TRANFORM !"></center>
                                   </div>
                                   </form>

                              </div>
                         </div>


                    </div>

               </div>
          </div>
     </section>

     <!-- Footer Section -->

     <footer>
          <div class="container">
               <div class="row">

                    <div class="col-md-5 col-md-offset-1 col-sm-6">
                         <h3>Team Member</h3>
                         <p>NYCU IIM</p>
                         <p>311706007 楊雅喬</p>
                         <p>3117060 陳婕儀</p>
                         <p>3117060 黃鈺吟</p>
                         <p>311706039 余雪華</p>
                    </div>

                    <div class="col-md-4 col-md-offset-1 col-sm-6">
                         <h3>Contact to us</h3>
                         <p>Contactor : NYCU IIM 余雪華</p>
                         <p>Email : hsueh6101.mg11@nycu.edu.tw</p>
                    </div>
               </div>
          </div>
     </footer>

     <!-- Back top -->
     <a href="#back-top" class="go-top"><i class="fa fa-angle-up"></i></a>

     <!-- SCRIPTS -->

     <script src="js/jquery.js"></script>
     <script src="js/bootstrap.min.js"></script>
     <script src="js/particles.min.js"></script>
     <script src="js/app.js"></script>
     <script src="js/jquery.parallax.js"></script>
     <script src="js/smoothscroll.js"></script>
     <script src="js/custom.js"></script>


</body>

</html>