此為產學合作案中的fuzzy模型
<br>在此模型主要會先透過問券向各分行經理人了解該分行的特性，並透過此特性建立fuzzy模型
<br>最後會透過模糊值來計算各分行的決策分數，以此來衡量各分行的運補急迫度
<br>

Bank_branches_cash_repository.csv 為進行測試之庫存水位資料 <br>
Bank_branches_fuzzy_sets.csv 為根據問卷向分行主管得知之分行特性，後續利用此特性進行fuzzy建模 <br>
執行fuzzy_model.py可以產生各分行之模糊值<br>
執行fuzzy_reasoning.py可以產生各分行之急迫度<br>

<br>test_fuzzy.py 為使用歷史資料測試fuzzy_model和fuzzy_reasoning
<br>測試後的決策分數用長條圖成，如output.png