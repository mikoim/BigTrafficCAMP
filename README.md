# BigTrafficCAMP
ビッグトラフィックCAMP@サイバーエージェント  
2015/05/16(土)~2015/05/17(日)  

## 構成
MariaDB 10.x <-> MySQLdb <-> Python 3.4.2 <-> Flask <-> Gunicorn <-> nginx

## 反省点
 * findByCardTagsIncludeAnyとsortByCardMatchedTagsNumが指定された時の適切な処理を実装できなかった．（SQLを復習すること）
 * データを正規化してテーブルに分けたが，分けすぎて十分なパフォーマンスが得られるまで持っていくことができなかった．（パフォーマンスの追求と汎用性を求めるのは別？）
