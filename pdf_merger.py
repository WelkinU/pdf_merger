from flask import Flask, render_template, redirect, send_file, url_for, flash
from forms import PDFForm
from PyPDF2 import PdfFileMerger
from io import BytesIO
import tempfile
import config
app = Flask(__name__)

app.config['SECRET_KEY'] = config.SECRET_KEY

def merge_pdfs(file_list, pages_list):
	assert len(file_list) == len(pages_list), '# of pdf files not equal to # of page lists to merge'

	print('merging pdfs')
	merger = PdfFileMerger()
	for file, page_list in zip(file_list, pages_list):

		page_list = page_list.replace(' ','') #strip spaces from the input
		if len(page_list)==0:
			continue

		#parse the input and append pages accordingly
		for txt in page_list.split(','):
			if '-' in txt:
				rng = txt.split('-')

				#note that 1 is the first page on the web interface, but 0 is first page in pypdf2
				merger.append(fileobj = file, pages = (int(float(rng[0]))-1,int(float(rng[1]))))
			else:
				merger.append(fileobj = file, pages = (int(float(txt))-1,int(float(txt))))

	return merger


@app.route('/', methods = ['GET','POST'])
@app.route('/home', methods = ['GET','POST'])
def home():
	form = PDFForm()
	if form.validate_on_submit():
		flash(f'Processing...', 'success')

		if form.pdf.data:
			print('----------- >>> MERGE STUFF HERE')
			merger = merge_pdfs([BytesIO(form.pdf.data.read())], [form.pages.data])

			merger.write(open(app.root_path + '/static/test_pdf/test.pdf','wb'))
			return send_file(app.root_path + '/static/test_pdf/test.pdf',as_attachment=True)

			'''
			#getting a MIME error when using a temp file...
			with tempfile.NamedTemporaryFile(delete=False) as temp:
				merger.write(temp)
				return send_file(temp)
			'''
		return redirect(url_for('home'))
	else:
		print(form.errors)
	return render_template('home.html', form = form)


@app.route('/about')
def about():
    return render_template('about.html', title = 'About')

if __name__ == '__main__':
	app.run(debug = True)