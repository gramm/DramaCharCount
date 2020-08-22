	<canvas id="jdtp_to_jlpt" width="20" height="10"></canvas>
	<canvas id="jltp_to_jdpt" width="20" height="10"></canvas>
	<button onclick="resetZoom()">Reset Zoom</button>
	
	<script>
		var chart_array = [];
		window.resetZoom = function() {
			chart_array[0].resetZoom();
			chart_array[1].resetZoom();
		};
	</script>
		
	<?php
		include("jdpt_jlpt_dist.js");	
	?>
		
	<script>
	 var current_chart = 'jdtp_to_jlpt';
	 var current_label = jdpt_5_to_jlpt_label;
	 var current_data = jdpt_5_to_jlpt_data;
	 var current_title = 'Distance of JDPT kanji compared to the equivalent JLPT level';
	</script>
	
	<?php
		include("chart_jdtp_to_jlpt.js");	
	?>
			
	<script>
	 var current_chart = 'jltp_to_jdpt';
	 var current_label = jlpt_5_to_jdpt_label;
	 var current_data = jlpt_5_to_jdpt_data;
	 var current_title = 'Distance of JLPT kanji compared to the equivalent JDPT level';
	</script>
	
	<?php
		include("chart_jdtp_to_jlpt.js");	
	?>
			
			
	<script>

</script>
	<div class="text-left blabla">
		<br /> 
		Below you can find the list of all JDPT 5 kanji.
		<br /> 
		<table class='table table-bordered table-striped table-sm'>
<tr>
<th>Kanji</th>
<th>Count</th>
<th>Frequency</th>
<th>JDPT</th>
</tr>
<tr><td>何</td><td>350371</td><td>1.6%</td><td>5</td></tr>
<tr><td>人</td><td>345650</td><td>1.5%</td><td>5</td></tr>
<tr><td>事</td><td>281434</td><td>1.2%</td><td>5</td></tr>
<tr><td>子</td><td>279614</td><td>1.2%</td><td>5</td></tr>
<tr><td>私</td><td>229281</td><td>1.0%</td><td>5</td></tr>
<tr><td>言</td><td>221538</td><td>1.0%</td><td>5</td></tr>
<tr><td>一</td><td>221117</td><td>1.0%</td><td>5</td></tr>
<tr><td>大</td><td>207848</td><td>0.9%</td><td>5</td></tr>
<tr><td>生</td><td>195934</td><td>0.9%</td><td>5</td></tr>
<tr><td>前</td><td>193123</td><td>0.9%</td><td>5</td></tr>
<tr><td>今</td><td>184521</td><td>0.8%</td><td>5</td></tr>
<tr><td>分</td><td>183538</td><td>0.8%</td><td>5</td></tr>
<tr><td>見</td><td>170920</td><td>0.8%</td><td>5</td></tr>
<tr><td>思</td><td>168304</td><td>0.7%</td><td>5</td></tr>
<tr><td>日</td><td>167096</td><td>0.7%</td><td>5</td></tr>
<tr><td>出</td><td>164503</td><td>0.7%</td><td>5</td></tr>
<tr><td>行</td><td>158479</td><td>0.7%</td><td>5</td></tr>
<tr><td>気</td><td>135095</td><td>0.6%</td><td>5</td></tr>
<tr><td>俺</td><td>133779</td><td>0.6%</td><td>5</td></tr>
<tr><td>先</td><td>129054</td><td>0.6%</td><td>5</td></tr>
<tr><td>本</td><td>124063</td><td>0.6%</td><td>5</td></tr>
<tr><td>来</td><td>123381</td><td>0.5%</td><td>5</td></tr>
<tr><td>手</td><td>121449</td><td>0.5%</td><td>5</td></tr>
<tr><td>田</td><td>119305</td><td>0.5%</td><td>5</td></tr>
<tr><td>間</td><td>116614</td><td>0.5%</td><td>5</td></tr>
<tr><td>話</td><td>111810</td><td>0.5%</td><td>5</td></tr>
<tr><td>時</td><td>107215</td><td>0.5%</td><td>5</td></tr>
<tr><td>長</td><td>106835</td><td>0.5%</td><td>5</td></tr>
<tr><td>君</td><td>100848</td><td>0.4%</td><td>5</td></tr>
<tr><td>会</td><td>100666</td><td>0.4%</td><td>5</td></tr>
<tr><td>女</td><td>99739</td><td>0.4%</td><td>5</td></tr>
<tr><td>中</td><td>97792</td><td>0.4%</td><td>5</td></tr>
<tr><td>上</td><td>96195</td><td>0.4%</td><td>5</td></tr>
<tr><td>自</td><td>91266</td><td>0.4%</td><td>5</td></tr>
<tr><td>者</td><td>84592</td><td>0.4%</td><td>5</td></tr>
<tr><td>方</td><td>83262</td><td>0.4%</td><td>5</td></tr>
<tr><td>入</td><td>81184</td><td>0.4%</td><td>5</td></tr>
<tr><td>部</td><td>80935</td><td>0.4%</td><td>5</td></tr>
<tr><td>美</td><td>79332</td><td>0.4%</td><td>5</td></tr>
<tr><td>当</td><td>79258</td><td>0.4%</td><td>5</td></tr>
<tr><td>合</td><td>78283</td><td>0.3%</td><td>5</td></tr>
<tr><td>知</td><td>76102</td><td>0.3%</td><td>5</td></tr>
<tr><td>音</td><td>75038</td><td>0.3%</td><td>5</td></tr>
<tr><td>家</td><td>74926</td><td>0.3%</td><td>5</td></tr>
<tr><td>年</td><td>73100</td><td>0.3%</td><td>5</td></tr>
<tr><td>理</td><td>72166</td><td>0.3%</td><td>5</td></tr>
<tr><td>目</td><td>69152</td><td>0.3%</td><td>5</td></tr>
<tr><td>聞</td><td>68421</td><td>0.3%</td><td>5</td></tr>
<tr><td>夫</td><td>67149</td><td>0.3%</td><td>5</td></tr>
<tr><td>下</td><td>66818</td><td>0.3%</td><td>5</td></tr>
<tr><td>山</td><td>66458</td><td>0.3%</td><td>5</td></tr>
<tr><td>男</td><td>66083</td><td>0.3%</td><td>5</td></tr>
<tr><td>待</td><td>65455</td><td>0.3%</td><td>5</td></tr>
<tr><td>野</td><td>65356</td><td>0.3%</td><td>5</td></tr>
<tr><td>僕</td><td>64892</td><td>0.3%</td><td>5</td></tr>
<tr><td>持</td><td>64834</td><td>0.3%</td><td>5</td></tr>
<tr><td>様</td><td>64297</td><td>0.3%</td><td>5</td></tr>
<tr><td>金</td><td>62923</td><td>0.3%</td><td>5</td></tr>
<tr><td>社</td><td>62729</td><td>0.3%</td><td>5</td></tr>
<tr><td>全</td><td>62700</td><td>0.3%</td><td>5</td></tr>
<tr><td>父</td><td>62102</td><td>0.3%</td><td>5</td></tr>
<tr><td>心</td><td>61710</td><td>0.3%</td><td>5</td></tr>
<tr><td>母</td><td>60296</td><td>0.3%</td><td>5</td></tr>
<tr><td>取</td><td>59734</td><td>0.3%</td><td>5</td></tr>
<tr><td>同</td><td>57684</td><td>0.3%</td><td>5</td></tr>
<tr><td>違</td><td>57386</td><td>0.3%</td><td>5</td></tr>
<tr><td>願</td><td>56168</td><td>0.2%</td><td>5</td></tr>
<tr><td>小</td><td>55985</td><td>0.2%</td><td>5</td></tr>
<tr><td>声</td><td>55885</td><td>0.2%</td><td>5</td></tr>
<tr><td>場</td><td>55156</td><td>0.2%</td><td>5</td></tr>
<tr><td>結</td><td>55089</td><td>0.2%</td><td>5</td></tr>
<tr><td>後</td><td>55070</td><td>0.2%</td><td>5</td></tr>
<tr><td>仕</td><td>54867</td><td>0.2%</td><td>5</td></tr>
<tr><td>真</td><td>54598</td><td>0.2%</td><td>5</td></tr>
<tr><td>誰</td><td>54069</td><td>0.2%</td><td>5</td></tr>
<tr><td>度</td><td>53739</td><td>0.2%</td><td>5</td></tr>
<tr><td>食</td><td>53568</td><td>0.2%</td><td>5</td></tr>
<tr><td>殺</td><td>53106</td><td>0.2%</td><td>5</td></tr>
<tr><td>川</td><td>52353</td><td>0.2%</td><td>5</td></tr>
</table>
	</div>