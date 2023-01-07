from flask import Flask, request, redirect, render_template

app = Flask(__name__)

docs = [
    {'id':1, "title":"김종호 폼 미쳤다", 'content':'첫 피모 깔끔'},
    {'id':2, "title":"김민재 굉장하다", 'content':'내 생애 첫 월드컵 16강인데 브라질임..브라질 이력: 아시아 국가한테 100년 동안 한번도 진적 없음'},
    {'id':3, "title":"중요한건 꺾이지 않는 마음", 'content':'처음으로 피모 tp 23억 모았는데 살게 비에이라 ^^.'}
]
nextId = len(docs) + 1


@app.route('/')
def index():
    html = '''<ul><li><a href="/create/">글쓰기</a></li></ul>'''
    return render_template('index.html', docs=docs)


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

    return render_template('read.html', docs=docs, title = title, content = content, id=id)

@app.route("/create/", methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        html = ''' <form action="/create/" method="POST">
            <p><input type='text' name="title" placeholder="제목"></p>
            <p><textarea name="content" style="width: 704px; height: 356px;"></textarea></p>
            <p><input type='submit' value='작성'></p>
        </form>'''
        return render_template('create.html', docs=docs)
    elif request.method == "POST":
        global nextId
        title=request.form['title']
        content=request.form['content']
        newDocs={'id':nextId, 'title':title, 'content':content}
        docs.append(newDocs)
        url = f'/read/{str(nextId)}/'
        nextId += 1
        return redirect(url)

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

    return render_template('update.html', docs=docs, title = title, id=id)

@app.route("/update/<int:id>/", methods=['POST'])
def update_post(id):
    for doc in docs:
        if id == doc['id']:
            doc['title'] = request.form['title']
            doc['content'] = request.form['content']
            break
    

    url = f'/read/{str(id)}/'
    return redirect(url)
