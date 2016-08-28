<?php
/**
 * databasename什么的自己写=-=
 *运行movie rank那个py之后就可以用这个
 */
header("Content-type: text/html; charset=utf-8"); 
$conn = @mysql_connect('localhost','root','newpass');
$dbs = @mysql_select_db('moviedouban');
$xxx = @mysql_query("SET NAMES UTF8");
$filess=scandir('./');
for($c=4;$c<count($filess);$c++){
	echo $filess[$c];
	$files = fopen($filess[$c],'r');
	$i=0;
	if($files) {
		while(!feof($files)){
			$table_name=explode('-', $filess[$c])[0];
			$buffer = fgets($files);
			// echo $table_name;
			$book_innnn = json_decode($buffer);
			$file_num = count($book_innnn);
			// exit();
			// echo $file_num;
			for($i=0;$i<$file_num;$i++){
				// echo '123';
			$movie_id = intval($book_innnn[$i]->id);
			$movie_name=$book_innnn[$i]->title;
			$movie_url = $book_innnn[$i]->url;
			$movie_type = implode(',', $book_innnn[$i]->types);
			$movie_regions = implode(',',$book_innnn[$i]->regions);
			$movie_release_date = $book_innnn[$i]->release_date;
			$type_rank = intval($book_innnn[$i]->rank);
			$movie_image = $book_innnn[$i]->cover_url;
			$movie_actor = implode(',', $book_innnn[$i]->actors);
			$movie_score = floatval($book_innnn[$i]->score);
			$vote_count = intval($book_innnn[$i]->vote_count);
			$rating_two = intval($book_innnn[$i]->rating[1]);


			$Insert_Str="INSERT INTO `".$table_name."`(`movie_id`, `movie_name`, `movie_url`, `movie_type`, `movie_regions`, `movie_release_date`, `type_rank`, `movie_image`, `movie_actor`, `movie_score`, `vote_count`, `rating_two`) VALUES (".$movie_id.",'".$movie_name."','".$movie_url."','".$movie_type."','".$movie_regions."','".$movie_release_date."',".$type_rank.",'".$movie_image."','".$movie_actor."',".$movie_score.",{$vote_count},{$rating_two})";

			mysql_query($Insert_Str);			
			}
			$i+=1;
		}
		fclose($files);
	}
}
mysql_close();

?>