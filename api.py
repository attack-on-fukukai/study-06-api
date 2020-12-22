import requests
import pandas as pd

def get_api(url):
    result = requests.get(url)
    return result.json()


def main():
    ## 課題1 以下の仕様を参考にして、任意のキーワードでAPIを検索した時の商品名と価格の一覧を取得してみましょう
    keyword = input("商品名と価格の一覧を取得したいキーワードを入力してください。")
    if len(keyword) > 0:
        url = f"https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?format=json&keyword={keyword}&applicationId=1019079537947262807"    
        result = get_api(url)

        for i in range(0, len(result["Items"])):
            # 商品名
            print(f"商品名：{result['Items'][i]['Item']['itemName']}")
            # 価格
            print(f"価格：￥{result['Items'][i]['Item']['itemPrice']:,}")


    ## 課題2 以下のAPIを使って、任意の商品の最安値と最高値を取得してみましょう
    keyword = ""
    keyword = input("最安値と最高値を取得したいキーワードを入力してください。")
    if len(keyword) > 0:
        url = f"https://app.rakuten.co.jp/services/api/Product/Search/20170426?format=json&keyword={keyword}&applicationId=1019079537947262807"
        result = get_api(url)
      
        for i in range(0, len(result["Products"])):
            # 製品名
            print(f"製品名：{result['Products'][i]['Product']['productName']}")
            # 最安値
            print(f"最安値：{result['Products'][i]['Product']['minPrice']:,}")
            # 最高値
            print(f"最高値：{result['Products'][i]['Product']['maxPrice']:,}")
  

    ## 課題3 以下のAPIを使って、任意のジャンルのランキング一覧を取得し、CSV出力してみましょう 
    #ジャンルの取得
    url = "https://app.rakuten.co.jp/services/api/IchibaGenre/Search/20140222?format=json&genreId=0&applicationId=1019079537947262807"
    result = get_api(url)
    genreList = []
    print("ジャンル一覧")
    for i in range(0, len(result["children"])):
        print(f"{result['children'][i]['child']['genreId']}：{result['children'][i]['child']['genreName']}")
        genreList.append(result["children"][i]["child"]["genreId"])

    genreId = input("ランキング一覧を取得したいジャンルIDを入力してください。")
    if len(genreId) > 0:

        # 実在するジャンルIDなのか確認する
        if int(genreId) in genreList:
            url = f"https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?format=json&genreId={genreId}&applicationId=1019079537947262807"
            result = get_api(url)

            rankList = []
            for i in range(0, len(result["Items"])):
                wrk_str = f"第{result['Items'][i]['Item']['rank']}位：{result['Items'][i]['Item']['itemName']}"
                print(wrk_str)
                rankList.append(wrk_str)

            df = pd.DataFrame(rankList)
            df.to_csv("rnk.csv",header=False,index=False)
        else:
            print("該当するジャンルIDがありません")


main()
