from flask import Flask, request, redirect

app = Flask(__name__)

docs = [
    {'id':1, "title":"김종호 폼 미쳤다", 'content':'첫 피모 깔끔'},
    {'id':2, "title":"김민재 굉장하다", 'content':'내 생애 첫 월드컵 16강인데 브라질임..브라질 이력: 아시아 국가한테 100년 동안 한번도 진적 없음'},
    {'id':3, "title":"중요한건 꺾이지 않는 마음", 'content':'처음으로 피모 tp 15억 모았는데 살게 없다.'}
]
nextId = len(docs) + 1


def template(html):
    oltag = '<ol>'
    for doc in docs:
        # oltag +=  '<li><a href="read/{}/">{}</a><li>'.format(doc['id'], doc['title'])
        oltag +=  f'<li><a href="/read/{doc["id"]}/">{doc["title"]}</a></li>'
    oltag += '</ol>'     

    return f'''<!DOCTYPE html>
        <html lang="ko">
        <head>
            <title>게시판</title>
        </head>
        <body>
            <h1>피파모바일</h1>
            <a href="/">게시판</a>
            {oltag}
            {html}
        </body>
        </html>'''



@app.route('/')
def index():
    html = '''<ul><li><a href="/create/">글쓰기</a></li></ul>'''
    return template(html)


@app.route('/reads/<int:id>/')
def reads(id):
    result = id + 1
    return str(result)

@app.route("/read/<int:id>/")
def read(id):
    title = ''
    content = ''
    for doc in docs:
        if doc['id'] == id:
            title = doc['title']
            content = doc['content']

    html = f'''<h1>{title}</h1>
    <p>{content}</p>
        <ul>
        <li><a href="/update/{id}/">수정</a></li>
        <li><form action="/delete/{id}/" method="POST">
            <input type="submit" value="삭제"></form>
    </li>
    </ul>
    '''

    return template(html)

@app.route("/create/", methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        html = ''' <form action="/create/" method="POST">
            <p><input type='text' name="title" placeholder="제목"></p>
            <p><textarea name="content" style="width: 704px; height: 356px;"></textarea></p>
            <p><input type='submit' value='작성'></p>
        </form>'''
    elif request.method == "POST":
        global nextId
        title=request.form['title']
        content=request.form['content']
        newDocs={'id':nextId, 'title':title, 'content':content}
        docs.append(newDocs)
        url = f'/read/{str(nextId)}/'
        nextId += 1
        return redirect(url)
    return template(html)

@app.route("/update/<int:id>/")
def update(id):
    title = ''
    content = ''
    for doc in docs:
        if doc['id'] == id:
            title = doc['title']
            content = doc['content']

    html = f'''
     <form action="/update/{id}/" method="POST">
            <p><input type='text' name="title" value="{title}"></p>
            <p><textarea name="content" style="width: 704px; height: 356px;">{content}</textarea></p>
            <p><input type='submit' value='수정'></p>
        </form>'''

    return template(html)

@app.route("/update/<int:id>/", methods=['POST'])
def update_post(id):
    for doc in docs:
        if id == doc['id']:
            doc['title'] = request.form['title']
            doc['content'] = request.form['content']
            break
    

    url = f'/read/{str(id)}/'
    return redirect(url)



@app.route("/delete/<int:id>/", methods=['POST'])
def delete(id):
    for doc in docs:
        if id == doc['id']:
            docs.remove(doc)
            break
    return redirect('/')



app.run(debug=True)
