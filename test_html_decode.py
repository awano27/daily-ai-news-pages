# テスト用のHTMLエンティティデコード確認
import html

# 文字化けの例
test_text = "&#32; &#32;によって提出されました  /u/metaknowing [link]&#32; [コメント]"
decoded_text = html.unescape(test_text)

print("元のテキスト:", test_text)
print("デコード後:", decoded_text)

# 別の文字化け例
test_text2 = "&amp;&#32; &amp;&#32;によって提出されました"
decoded_text2 = html.unescape(test_text2)

print("\n元のテキスト2:", test_text2)
print("デコード後2:", decoded_text2)

# さらなる文字化け例
test_text3 = "＆amp;＃32;"
decoded_text3 = html.unescape(test_text3)

print("\n元のテキスト3:", test_text3)
print("デコード後3:", decoded_text3)