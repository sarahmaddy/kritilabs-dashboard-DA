from flask import Flask,render_template,redirect,request,flash,url_for,send_from_directory
from werkzeug.utils import secure_filename
import os

company_names=['Jharsuguda-OSO-IOC', 'Ramagundam-TAPSO-IOC', 'Bangalore-KASO-IOC',
       'Panipat-DSO-IOC', 'Khunti-BSO-IOC', 'Tikrikalan-DSO-IOC',
       'Gulbarga-KASO-IOC', 'Jasidih-BSO-IOC', 'Doimukh-IO-AOD-IOC',
       'Meerut-UPSO2-IOC', 'Pune-MSO-IOC', 'Allahabad-UPSO1-IOC',
       'Tondiarpet-TNSO-IOC', 'UNA-PSO-IOC', 'Korba-MPSO-IOC',
       'Madurai-TNSO-IOC', 'Cochin-KESO-IOC', 'Chandrapur-MSO-IOC',
       'Jhansi-UPSO1-IOC', 'Rajbandh-WBSO-IOC', 'Betkuchi-IO-AOD-IOC',
       'Kanpur-UPSO1-IOC', 'Barauni-BSO-IOC', 'Gwalior-MPSO-IOC',
       'ETTPL-TNSO-IOC', 'Mughalsarai-UPSO1-IOC', 'Solapur-MSO-IOC',
       'Lucknow-UPSO1-IOC', 'Mourigram-WBSO-IOC', 'Bhatinda-PSO-IOC',
       'Ongole-TAPSO-IOC', 'Jammu depot-J&K-IOC', 'Aonla-UPSO2-IOC',
       'Dumad-GSO-IOC', 'Ahmadnagar-MSO-IOC', 'Malom-IO-AOD-IOC',
       'Miraj-MSO-IOC', 'Guwahati RC-AOD-IOC', 'Jodhpur-RSO-IOC',
       'Najibabad-UPSO2-IOC', 'Bakania-MPSO-IOC', 'Jabalpur-MPSO-IOC',
       'Jalandhar-PSO-IOC', 'Ahmedabad-GSO-IOC', 'Hyderabad-TAPSO-IOC',
       'Vijayawada-TAPSO-IOC', 'Malda-WBSO-IOC', 'Akola-MSO-IOC',
       'Mathura-UPSO2-IOC', 'Ratlam-MPSO-IOC', 'Sagar-MPSO-IOC',
       'Trichy-TNSO-IOC', 'Chittorgarh-RSO-IOC', 'Paradeep-OSO-IOC',
       'Sankari-TNSO-IOC', 'Jaipur-RSO-IOC', 'Vashi-MSO-IOC',
       'Bijapur-KASO-IOC', 'Rangpo-WBSO-IOC', 'Jatni-OSO-IOC',
       'Manmad-MSO-IOC', 'Mangalore-KASO-IOC', 'Lakholi-MPSO-IOC',
       'Haldia B-WBSO-IOC', 'Hassan-KASO-IOC', 'Patna-BSO-IOC',
       'Bharatpur-RSO-IOC', 'Vairangte-IO-AOD-IOC', 'Golai-IO-AOD-IOC',
       'Rewari-DSO-IOC', 'Hubli-KASO-IOC', 'Chittoor-TAPSO-IOC',
       'Kozhikode-KESO-IOC', 'Sangrur-PSO-IOC', 'Vadinar-GSO-IOC',
       'JNPT-MSO-IOC', 'Gonda-UPSO1-IOC', 'Belgaum-KASO-IOC',
       'Wadala-MSO-IOC', 'Sidhpur-GSO-IOC', 'Agra-UPSO2-IOC',
       'Vizag-TAPSO-IOC', 'Baitalpur-UPSO1-IOC', 'Moinarbond-IO-AOD-IOC',
       'Port blair-WBSO-IOC', 'Rajahmundry-TAPSO-IOC',
       'Siliguri-WBSO-IOC', 'Bongaigaon-IO-AOD-IOC', 'EXMI customer',
       'ZIOL-Vasco-MSO-IOC', 'Hazira-GSO-IOC', 'Haldia-Refinery-WBSO-IOC',
       'Indore-MPSO-IOC', 'Jayant-MPSO-IOC', 'Lumding-IO-AOD-IOC',
       'Dimapur-IO-AOD-IOC', 'Missamari-IO-AOD-IOC', 'Roorkee-UPSO2-IOC',
       'Banthra-UPSO2-IOC', 'KFST-GSO-IOC', 'Lalkuan-UPSO2-IOC',
       'Dhule-MSO-IOC', 'Guntakal-TAPSO-IOC', 'Warangal-TAPSO-IOC',
       'Vasco-MSO-IOC', 'Dharmanagar-IO-AOD-IOC',
       'Mangalore ASP-KASO-IOC', 'Itarsi-MPSO-IOC', 'Asanur-TNSO-IOC',
       'Rajkot-GSO-IOC', 'Coimbatore-TNSO-IOC', 'NELWardha-MSO-IOC',
       'Balasore-OSO-IOC', 'Borkhedi-MSO-IOC', 'Mysore-KASO-IOC',
       'Tondiarpet-Lubes-IOC', 'Sewree-MSO-IOC', 'Motihari-BSO-IOC',
       'Wellington-KESO-IOC', 'Koyali-GSO-IOC', 'Suryapet-TAPSO-IOC',
       'Kritilabs Test']

months=["Jan","Feb","Mar","Apr","May","Jun","July","Aug","Sep","Oct","Nov","Dec"]

years=[2018,2019,2022,2023,2024]

states=['UPSO1','GSO','OSO','MSO','DSO','MPSO','RSO','KASO','WBSO','BSO','AOD','PSO','TNSO','UPSO2','TAPSO']


app=Flask(__name__)
app.config["SECRET_KEY"]='SUPERSECRETKEY'
app.config['UPLOAD_FOLDER']="static/files"

@app.route("/")
def home():
  return render_template('home.html')
  
@app.route("/company")
def company():  
  return render_template('company_name.html',company_names=company_names,months=months,years=years)

@app.route("/company_analysis",methods=["GET","POST"])
def company_analysis():
  if request.method == 'POST':
    as_dict1 = request.form.getlist('field1')
    as_dict2 = request.form.getlist('field2')
    as_dict3 = request.form.getlist('field3')
    print (as_dict1,as_dict2,as_dict3,type(as_dict1),type(as_dict2))
    file=request.files['file1']
    ffile=request.files["file2"]
    location1=os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config["UPLOAD_FOLDER"],secure_filename(file.filename))
    file.save(location1)
    
    location2=os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config["UPLOAD_FOLDER"],secure_filename(ffile.filename))  
  
    ffile.save(location2)
    return as_dict1,"file has been uploaded successfully"


@app.route("/state")
def state():
  return render_template('state_names.html',states=states,months=months,years=years)



@app.route("/state_analysis",methods=["GET","POST"])
def state_analysis():
  if request.method == 'POST':
    as_dict1 = request.form.getlist('field1')
    as_dict2 = request.form.getlist('field2')
    as_dict3 = request.form.getlist('field3')
    print (as_dict1,as_dict2,as_dict3,type(as_dict1),type(as_dict2))
    file=request.files['file1']
    ffile=request.files["file2"]
    location1=os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config["UPLOAD_FOLDER"],secure_filename(file.filename))
    file.save(location1)
    location2=os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config["UPLOAD_FOLDER"],secure_filename(ffile.filename))
    ffile.save(location2)

    from state_analysis import state_call_analysis

    result=state_call_analysis(location1,location2,as_dict1,as_dict2,as_dict3)
  
    return send_from_directory("output","state analysis.csv")






if __name__=="__main__":
  app.run(host="0.0.0.0",debug=True)