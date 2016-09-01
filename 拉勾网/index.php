
<?php
header("Content-type: text/html; charset=utf-8"); 
$conn = @mysql_connect('localhost','root','newpass');
$dbs = @mysql_select_db('lagou');
$xxx = @mysql_query("SET NAMES UTF8");

$filess=scandir('./lagoujob');
// print_r($filess);
$x = 0;
$y = 0;


for($x = 2;$x<count($filess);$x++){
	$filename = iconv('GBK', 'UTF-8', $filess[$x]);
	$y+=1;
	$z= 0;

	$files = fopen('./lagoujob/'.iconv('UTF-8','GBK',$filename), 'r');
	// echo $filename;
	if($files){
		while(!feof($files)){
			$buffer  = fgets($files);
			// echo $buffer;exit();
			// echo $buffer;
			$z+=1;
			$lagou_inner = json_decode($buffer);
			// var_dump($lagou_inner->content->positionResult->result[0]);
			$result_info = @$lagou_inner->content->positionResult->result;
			for($i=0;$i<count($result_info);$i++){
				$lagou_positionId=$result_info[$i]->positionId;
				// echo $buffer;
				$lagou_positionName=$result_info[$i]->positionName;
				$lagou_education=$result_info[$i]->education;
				$lagou_jobNature = $result_info[$i]->jobNature;
				$lagou_workYear = $result_info[$i]->workYear;
				$lagou_createTime = $result_info[$i]->createTime;
				$lagou_companyShortName = $result_info[$i]->companyShortName;
				$lagou_companyId = $result_info[$i]->companyId;
				$lagou_salary = $result_info[$i]->salary;
				$lagou_city = $result_info[$i]->city;
				$lagou_positionAdvantage = $result_info[$i]->positionAdvantage;
				$lagou_companyLogo = $result_info[$i]->companyLogo;
				$lagou_industryField = $result_info[$i]->industryField;
				if(is_array($result_info[$i]->companyLabelList)){
					$lagou_companyLabelList = implode(',',$result_info[$i]->companyLabelList);
				}
				else{
					$lagou_companyLabelList=$result_info[$i]->companyLabelList;
				}
				$lagou_financeStage = $result_info[$i]->financeStage;
				$lagou_district = $result_info[$i]->district;
				$lagou_companySize = $result_info[$i]->companySize;
				$lagou_companyFullName=$result_info[$i]->companyFullName;
				$lagou_lastLogin=$result_info[$i]->lastLogin;

				// $lagou_businessZones=;
				if(is_array($result_info[$i]->businessZones)){
					$lagou_businessZones=implode(',', $result_info[$i]->businessZones);
					// exit();
				}else{
					$lagou_businessZones = $result_info[$i]->businessZones;
				}
				$lagou_formatCreateTime=$result_info[$i]->formatCreateTime;
				$lagou_imState=$result_info[$i]->imState;
				$lagou_score=$result_info[$i]->score;
				$lagou_adWord=$result_info[$i]->adWord;
				$lagou_explain=$result_info[$i]->explain;
				$lagou_plus=$result_info[$i]->plus;
				$lagou_pcShow=$result_info[$i]->pcShow;
				$lagou_appShow=$result_info[$i]->appShow;
				$lagou_deliver=$result_info[$i]->deliver;
				$lagou_gradeDescription=$result_info[$i]->gradeDescription;
				$lagou_approve=$result_info[$i]->approve;
				$lagou_publisherId=$result_info[$i]->publisherId;

				$sql = "INSERT INTO `position`(`lagou_positionId`, `lagou_positionName`, `lagou_education`, `lagou_jobNature`, `lagou_workYear`, `lagou_createTime`, `lagou_companyShortName`, `lagou_companyId`, `lagou_salary`, `lagou_city`, `lagou_positionAdvantage`, `lagou_companyLogo`, `lagou_industryField`, `lagou_companyLabelList`, `lagou_financeStage`, `lagou_district`, `lagou_companySize`, `lagou_companyFullName`, `lagou_lastLogin`, `lagou_businessZones`, `lagou_formatCreateTime`, `lagou_imState`, `lagou_score`, `lagou_adWord`, `lagou_explain`, `lagou_plus`, `lagou_pcShow`, `lagou_appShow`, `lagou_deliver`, `lagou_gradeDescription`, `lagou_approve`, `lagou_publisherId`) VALUES ({$lagou_positionId},'{$lagou_positionName}','{$lagou_education}','{$lagou_jobNature}','{$lagou_workYear}','{$lagou_createTime}','{$lagou_companyShortName}',$lagou_companyId,'{$lagou_salary}','{$lagou_city}','{$lagou_positionAdvantage}','{$lagou_companyLogo}','{$lagou_industryField}','{$lagou_companyLabelList}','{$lagou_financeStage}','{$lagou_district}','{$lagou_companySize}','{$lagou_companyFullName}',$lagou_lastLogin,'{$lagou_businessZones}','{$lagou_formatCreateTime}','{$lagou_imState}',$lagou_score,$lagou_adWord,'{$lagou_explain}','{$lagou_plus}',$lagou_pcShow,$lagou_appShow,$lagou_deliver,'{$lagou_gradeDescription}',$lagou_approve,$lagou_publisherId)";
	// echo $sql;
			mysql_query($sql);
			// exit();
			}
		}
		
	}
	fclose($files);
	echo $filename.'       '.$z.'  行被读取<br/>';
}

echo $y.'本书被开启';

mysql_close();
?>