from re import search
from flask import Flask, render_template, redirect, url_for, Blueprint, flash, request
from flask_ckeditor import CKEditorField
import flask
from flask_wtf import form
from sim import app,db,bcrypt
from sim.admin.forms import daftar_admin,berita_F, data_umum, data_sekolah, akreditas_sekolah, kecamatan_sekolah, pengaduan_F, login_admin, profil_edit, berita_edit, data_umumedit, data_sekolahedit, akreditas_sekolahedit, kecamatan_sekolahedit,informasi_F, kegiatan_F, informasi_edit,kegiatan_edit,edit_admin,filter_dtumum,df_admin, profil
from sim.models import Tprofil, Tdataumum, Tdatasekolah, Takresklh, Tkecamatan, Tpengaduan, Tadmin, Tberita,Tdata_kegiatan,Tinformasi,Tdataumumfilter
import os
import secrets
from flask_login import login_user, current_user, logout_user, login_required
from sim import app
from PIL import Image

gadmin= Blueprint('gadmin',__name__)

def simpan_foto(form_foto):
    random_hex=secrets.token_hex(8)
    f_name, f_ext= os.path.splitext(form_foto.filename)
    foto_fn=random_hex + f_ext
    foto_path=os.path.join(app.root_path, 'sim/static/foto', foto_fn)
    ubah_size=(400,300)
    j=Image.open(form_foto)
    j.thumbnail(ubah_size)
    j.save(foto_path)
    #form_foto.save(foto_path)
    return foto_fn

@gadmin.route("/tes")
@login_required
def tes():
    return "Selamat datang di pelatihan"

@gadmin.route("/dashboard-admin")
@login_required
def dashboard():
    sekolah=len(Tdatasekolah.query.all())
    data_umum=len(Tdataumum.query.all())
    pengaduan=len(Tpengaduan.query.all())
    informasi=len(Tinformasi.query.all())
    kegiatan=len(Tdata_kegiatan.query.all())
    berita=len(Tberita.query.all())
    return render_template("t_admin/base.html", sekolah=sekolah, data_umum=data_umum, pengaduan=pengaduan, informasi=informasi,kegiatan=kegiatan, berita=berita)

#bagian PROFIL


@gadmin.route("/profil-admin", methods=['GET', 'POST'])
@login_required
def profill():
    form=profil()
    data=Tprofil.query.all()
    if form.validate_on_submit():
        add= Tprofil(sambutan=form.sambutan.data,visi=form.visi.data,misi=form.misi.data)
        db.session.add(add)
        db.session.commit()
        flash('Data berhasil ditambahkan','warning')
        return redirect(url_for('gadmin.profill'))
    return render_template("t_admin/sambutan.html", dataprofil=data, form=form)

@gadmin.route("/editprofil-admin/<int:ed_id>/update", methods=['GET', 'POST'])
@login_required
def profill_edit(ed_id):
    form=profil_edit()
    dataprofil=Tprofil.query.get_or_404(ed_id)
    if request.method=="GET":
        form.sambutan.data=dataprofil.sambutan
        form.visi.data=dataprofil.visi
        form.misi.data=dataprofil.misi
    elif form.validate_on_submit():
        dataprofil.sambutan=form.sambutan.data
        dataprofil.visi=form.visi.data 
        dataprofil.misi=form.misi.data   
        db.session.commit()
        flash('Data Berhasil Di ubah','warning')
        return redirect(url_for('gadmin.profill'))
    return render_template("t_admin/sambutan-edit.html", form=form)

@gadmin.route("/detail-profil/<int:ed_id>/detail", methods=['GET', 'POST'])
@login_required
def detail_profil(ed_id):
    dataprofil=Tprofil.query.get_or_404(ed_id)
    return render_template("t_admin/detail-profil.html", dataprofil=dataprofil)

@gadmin.route("/profil/<id>", methods=['GET', 'POST'])
@login_required
def hapus_profil(id):
    h_profil= Tprofil.query.get(id)
    db.session.delete(h_profil)
    db.session.commit()
    flash('Data berhasil dihapus', 'warning')
    return redirect(url_for('gadmin.profill'))



#Bagian BERITA
@gadmin.route("/berita-admin", methods=['GET', 'POST'], defaults={"page": 1})
@gadmin.route("/berita-admin/<int:page>", methods=['GET', 'POST'])
@login_required
def berita(page):
    form=berita_F()
    page = page
    pages = 10
    data=Tberita.query.all()
    berita = Tberita.query.order_by(Tberita.id.desc()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        berita = Tberita.query.filter(Tberita.judul.like(search)).paginate(page, pages, error_out=False)
        return render_template("t_admin/berita.html", berita=berita, form=form, tag=tag)
    if form.validate_on_submit():
        filefoto=simpan_foto(form.foto.data)
        add= Tberita(judul=form.judul.data,berita=form.berita.data,foto=filefoto)
        db.session.add(add)
        db.session.commit()
        flash('Data berhasil ditambahkan','warning')
        return redirect(url_for('gadmin.berita'))
    return render_template("t_admin/berita.html", databerita=data, form=form, berita=berita)

@gadmin.route("/editberita-admin/<int:ed_id>/update", methods=['GET', 'POST'])
@login_required
def berita_editt(ed_id):
    databerita=Tberita.query.get_or_404(ed_id)
    form=berita_edit()
    if request.method=="GET":
        form.judul.data=databerita.judul
        form.berita.data=databerita.berita
        form.foto.data=databerita.foto
    elif form.validate_on_submit():
        filefoto=simpan_foto(form.foto.data)
        databerita.judul=form.judul.data
        databerita.berita=form.berita.data
        databerita.foto=filefoto
        db.session.commit()
        flash('Data Berhasil Di ubah','warning')
        return redirect(url_for('gadmin.berita'))
    return render_template("t_admin/berita-edit.html", form=form)

@gadmin.route("/detail-databerita/<int:ed_id>/detail", methods=['GET', 'POST'])
@login_required
def berita_detail(ed_id):
    databerita=Tberita.query.get_or_404(ed_id)
    return render_template("t_admin/berita-detail.html", databerita=databerita)

@gadmin.route("/beritah/<id>", methods=['GET', 'POST'])
@login_required
def hapus_berita(id):
    h_berita= Tberita.query.get(id)
    db.session.delete(h_berita)
    db.session.commit()
    flash('Data berhasil dihapus', 'warning')
    return redirect(url_for('gadmin.berita'))


#bagian DATA UMUM
@gadmin.route("/dataumum-admin", methods=['GET', 'POST'], defaults={"page": 1})
@gadmin.route("/dataumum-admin/<int:page>", methods=['GET', 'POST'])
@login_required
def dataumuum(page):
    form=data_umum()
    page = page
    pages = 7
    data=Tdataumum.query.all()
    dataumum = Tdataumum.query.order_by(Tdataumum.id.desc()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        dataumum = Tdataumum.query.filter(Tdataumum.tahun.like(search)).paginate(page, pages, error_out=False)
        return render_template("t_admin/data-umum.html", dataumum=dataumum, form=form, tag=tag)
    if form.validate_on_submit():
        add= Tdataumum(tahun=form.tahun.data,jsekolah=form.jlh_sekolah.data,jsswasta=form.jlh_sswasta.data,jssnegeri=form.jlh_snegeri.data,jguru=form.jlh_guru.data,
        jgpns=form.jlh_gpns.data,jghonor=form.jlh_ghonor.data,jkepsek=form.jlh_kepsek.data, jkeppns=form.jlh_kpns.data, jkephonor=form.jlh_khonor.data,
        jrombel=form.jlh_rombel.data)
        db.session.add(add)
        db.session.commit()
        flash('Data berhasil ditambahkan','warning')
        return redirect(url_for('gadmin.dataumuum'))
    return render_template("t_admin/data-umum.html", dataumumm=data, form=form, dataumum=dataumum)


@gadmin.route("/dtfilter-admin", methods=['GET', 'POST'])
@login_required
def dtumum_filter():
    form=filter_dtumum()
    data=Tdataumumfilter.query.all()
    if form.validate_on_submit():
        add= Tdataumumfilter(tahun=form.tahun.data)
        db.session.add(add)
        db.session.commit()
        flash('Data Berhasil Di ubah','warning')
        return redirect(url_for('gadmin.dtumum_filter'))
    return render_template("t_admin/filter-dtumum.html", dataumum=data, form=form)

@gadmin.route("/dtfilteredit-admin/<int:ed_id>/update", methods=['GET', 'POST'])
@login_required
def dtumum_filteredit(ed_id):
    datafilter=Tdataumumfilter.query.get_or_404(ed_id)
    form=filter_dtumum()
    if request.method=="GET":
        form.tahun.data=datafilter.tahun
    elif form.validate_on_submit():
        datafilter.tahun=form.tahun.data
        db.session.commit()
        flash('Data Berhasil Di ubah','warning')
        return redirect(url_for('gadmin.dtumum_filter'))
    return render_template("t_admin/filter-dtumumedit.html", form=form)

@gadmin.route("/dtumumfilter/<id>", methods=['GET', 'POST'])
@login_required
def hapus_dtumumfilter(id):
    h_filter= Tdataumumfilter.query.get(id)
    db.session.delete(h_filter)
    db.session.commit()
    flash('Data berhasil dihapus', 'warning')
    return redirect(url_for('gadmin.dtumum_filter'))

@gadmin.route("/dataumumedit-admin/<int:ed_id>/update", methods=['GET', 'POST'])
@login_required
def dataumum_edit(ed_id):
    dataumum=Tdataumum.query.get_or_404(ed_id)
    form=data_umumedit()
    if request.method=="GET":
        form.tahun.data=dataumum.tahun
        form.jlh_sekolah.data=dataumum.jsekolah
        form.jlh_sswasta.data=dataumum.jsswasta
        form.jlh_snegeri.data=dataumum.jssnegeri
        form.jlh_guru.data=dataumum.jguru
        form.jlh_gpns.data=dataumum.jgpns
        form.jlh_ghonor.data=dataumum.jghonor
        form.jlh_kepsek.data=dataumum.jkepsek
        form.jlh_kpns.data=dataumum.jkeppns
        form.jlh_khonor.data=dataumum.jkephonor
        form.jlh_rombel.data=dataumum.jrombel
    elif form.validate_on_submit():
        dataumum.tahun=form.tahun.data
        dataumum.jsekolah=form.jlh_sekolah.data
        dataumum.jsswasta=form.jlh_sswasta.data
        dataumum.jssnegeri=form.jlh_snegeri.data 
        dataumum.jguru=form.jlh_guru.data
        dataumum.jgpns=form.jlh_gpns.data
        dataumum.jghonor=form.jlh_ghonor.data  
        dataumum.jkepsek=form.jlh_kepsek.data
        dataumum.jkeppns=form.jlh_kpns.data
        dataumum.jkephonor=form.jlh_khonor.data 
        dataumum.jrombel=form.jlh_rombel.data  
        db.session.commit()
        flash('Data Berhasil Di ubah','warning')
        return redirect(url_for('gadmin.dataumuum'))
    return render_template("t_admin/data-umumedit.html", form=form)

@gadmin.route("/detail-dataumum/<int:ed_id>/detail", methods=['GET', 'POST'])
@login_required
def detail_dataumum(ed_id):
    dataumum=Tdataumum.query.get_or_404(ed_id)
    return render_template("t_admin/data-umumdetail.html", dataumum=dataumum)

    
@gadmin.route("/dataumuum/<id>", methods=['GET', 'POST'])
@login_required
def hapus_dataumum(id):
    h_dataumum=Tdataumum.query.get(id)
    db.session.delete(h_dataumum)
    db.session.commit()
    flash('Data berhasil dihapus', 'warning')
    return redirect(url_for('gadmin.dataumuum'))


#bagian DATA SEKOLAH
@gadmin.route("/datasekolah-admin", methods=['GET', 'POST'], defaults={"page": 1})
@gadmin.route("/datasekolah-admin/<int:page>", methods=['GET', 'POST'])
@login_required
def sekolah(page):
    form=data_sekolah()
    page = page
    pages = 10
    datasekolah=Tdatasekolah.query.all()
    form.kecamatan.choices = [(str(tkecamatan.id), tkecamatan.jenis_wilayah) for tkecamatan in Tkecamatan.query.all()]
    form.akreditas.choices = [(str(takresklh.id), takresklh.jenis_akreditas) for takresklh in Takresklh.query.all()]
    sekolah = Tdatasekolah.query.order_by(Tdatasekolah.id.desc()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        sekolah = Tdatasekolah.query.filter(Tdatasekolah.npsn.like(search)).paginate(page, pages, error_out=False)
        return render_template("t_admin/data-sekolah.html", sekolah=sekolah, form=form, tag=tag)
    if form.validate_on_submit():
        file_foto=simpan_foto(form.foto.data)
        add= Tdatasekolah(npsn=form.npsn.data, sekolah=form.nama_sekolah.data, alamat=form.alamat.data, kecamatan_id=form.kecamatan.data,
        akresklh_id=form.akreditas.data, jenissklh=form.jenis_sekolah.data, namakepsek=form.nama_kepsek.data, foto=file_foto)
        db.session.add(add)
        db.session.commit()
        flash('Data berhasil ditambahkan','warning')
        return redirect(url_for('gadmin.sekolah'))
    return render_template("t_admin/data-sekolah.html", datasekolah=datasekolah, form=form, sekolah=sekolah)

@gadmin.route("/datasekolahedit-admin/<int:ed_id>/update", methods=['GET', 'POST'])
@login_required
def datasekolah_edit(ed_id):
    datasekolah=Tdatasekolah.query.get_or_404(ed_id)  
    form=data_sekolahedit()
    form.kecamatan.choices = [(str(tkecamatan.id), tkecamatan.jenis_wilayah) for tkecamatan in Tkecamatan.query.all()]
    form.akreditas.choices = [(str(takresklh.id), takresklh.jenis_akreditas) for takresklh in Takresklh.query.all()]
    if request.method=="GET":
        form.npsn.data=datasekolah.npsn
        form.nama_sekolah.data=datasekolah.sekolah
        form.alamat.data=datasekolah.alamat
        form.jenis_sekolah.data=datasekolah.jenissklh
        form.nama_kepsek.data=datasekolah.namakepsek
        form.akreditas.data=datasekolah.akresklh_id
        form.kecamatan.data=datasekolah.kecamatan_id
    elif form.validate_on_submit():
        file_foto=simpan_foto(form.foto.data)
        datasekolah.npsn=form.npsn.data
        datasekolah.sekolah=form.nama_sekolah.data
        datasekolah.alamat=form.alamat.data 
        datasekolah.jenissklh=form.jenis_sekolah.data
        datasekolah.namakepsek=form.nama_kepsek.data
        datasekolah.akresklh_id=form.akreditas.data  
        datasekolah.kecamatan_id=form.kecamatan.data
        datasekolah.foto=file_foto
        db.session.commit()
        flash('Data Berhasil Di ubah','warning')
        return redirect(url_for('gadmin.sekolah'))
    return render_template("t_admin/data-sekolahedit.html", form=form)

@gadmin.route("/detail-datasekolahh/<int:ed_id>/detail", methods=['GET', 'POST'])
@login_required
def datasekolah_detail(ed_id):
    datasekolah=Tdatasekolah.query.get_or_404(ed_id)
    return render_template("t_admin/data-sekolahdetail.html", datasekolah=datasekolah)

@gadmin.route("/datasekolah/<id>", methods=['GET', 'POST'])
@login_required
def hapus_sekolah(id):
    h_sekolah= Tdatasekolah.query.get(id)
    db.session.delete(h_sekolah)
    db.session.commit()
    flash('Data berhasil dihapus', 'warning')
    return redirect(url_for('gadmin.sekolah'))



#DATA AKREDITASI
@gadmin.route("/akreditassekolah-admin", methods=['GET', 'POST'])
@login_required
def akreditas():
    form=akreditas_sekolah()
    data=Takresklh.query.all()
    if form.validate_on_submit():
        add= Takresklh(jenis_akreditas=form.jenis_akreditas.data, informasi_akreditas=form.informasi_akreditas.data)
        db.session.add(add)
        db.session.commit()
        flash('Data berhasil ditambahkan','warning')
        return redirect(url_for('gadmin.akreditas'))
    return render_template("t_admin/akreditas-sekolah.html", dataakreditas=data, form=form)

@gadmin.route("/akreditassekolahedit-admin/<int:ed_id>/update", methods=['GET', 'POST'])
@login_required
def dataakreditas_edit(ed_id):
    dataakreditas=Takresklh.query.get_or_404(ed_id)
    form=akreditas_sekolahedit()
    if request.method=="GET":
        form.jenis_akreditas.data=dataakreditas.jenis_akreditas
        form.informasi_akreditas.data=dataakreditas.informasi_akreditas
    elif form.validate_on_submit():
        dataakreditas.jenis_akreditas=form.jenis_akreditas.data
        dataakreditas.informasi_akreditas=form.informasi_akreditas.data
        db.session.commit()
        flash('Data Berhasil Di ubah','warning')
        return redirect(url_for('gadmin.akreditas'))
    return render_template("t_admin/akreditas-sekolahedit.html", form=form)

@gadmin.route("/detail-dataakreditas/<int:ed_id>/detail", methods=['GET', 'POST'])
@login_required
def dataakreditas_detail(ed_id):
    dataakreditas=Takresklh.query.get_or_404(ed_id)
    return render_template("t_admin/akreditas-sekolahdetail.html", dataakreditas=dataakreditas)

@gadmin.route("/akreditas/<id>", methods=['GET', 'POST'])
@login_required
def hapus_akreditas(id):
    h_akreditas= Takresklh.query.get(id)
    db.session.delete(h_akreditas)
    db.session.commit()
    flash('Data berhasil dihapus', 'warning')
    return redirect(url_for('gadmin.akreditas'))



#DATA KECAMATAN
@gadmin.route("/alamatsekolah-admin", methods=['GET', 'POST'])
@login_required
def alamatsekolah():
    form=kecamatan_sekolah()
    data=Tkecamatan.query.all()
    if form.validate_on_submit():
        add= Tkecamatan(jenis_wilayah=form.jenis_wilayah.data, informasi_wilayah=form.informasi_wilayah.data)
        db.session.add(add)
        db.session.commit()
        flash('Data berhasil ditambahkan','warning')
        return redirect(url_for('gadmin.alamatsekolah'))
    return render_template("t_admin/alamat-sekolah.html", dataalamatsekolah=data, form=form)

@gadmin.route("/alamatsekolahedit-admin/<int:ed_id>/update", methods=['GET', 'POST'])
@login_required
def alamatsekolah_edit(ed_id):
    dataalamat=Tkecamatan.query.get_or_404(ed_id)
    form=kecamatan_sekolahedit()
    if request.method=="GET":
        form.jenis_wilayah.data=dataalamat.jenis_wilayah
        form.informasi_wilayah.data=dataalamat.informasi_wilayah
    elif form.validate_on_submit():
        dataalamat.jenis_wilayah=form.jenis_wilayah.data
        dataalamat.informasi_wilayah=form.informasi_wilayah.data
        db.session.commit()
        flash('Data Berhasil Di ubah','warning')
        return redirect(url_for('gadmin.alamatsekolah'))
    return render_template("t_admin/alamat-sekolahedit.html", form=form)


@gadmin.route("/alamatsekolah-detail/<int:ed_id>/detail", methods=['GET', 'POST'])
@login_required
def alamatsekolah_detail(ed_id):
    dataalamat=Tkecamatan.query.get_or_404(ed_id)
    return render_template("t_admin/alamat-sekolahdetail.html", dataalamat=dataalamat)

@gadmin.route("/alamat/<id>", methods=['GET', 'POST'])
@login_required
def hapus_alamat(id):
    h_alamat= Tkecamatan.query.get(id)
    db.session.delete(h_alamat)
    db.session.commit()
    flash('Data berhasil dihapus', 'warning')
    return redirect(url_for('gadmin.alamatsekolah'))



#PENGADUAN 
@gadmin.route("/pengaduan-admin", methods=['GET', 'POST'], defaults={"page": 1})
@gadmin.route("/pengaduan-admin/<int:page>", methods=['GET', 'POST'])
@login_required
def pengaduan(page):
    page = page
    pages = 7
    data=Tpengaduan.query.all()
    pengaduan = Tpengaduan.query.order_by(Tpengaduan.id.desc()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search ="%{}%".format(tag)
        pengaduan = Tpengaduan.query.filter(Tpengaduan.kategori.like(search)).paginate(page, pages, error_out=False)
        return render_template("t_admin/pengaduan.html", pengaduan=pengaduan, form=form, tag=tag)
    return render_template("t_admin/pengaduan.html", datapengaduan=data, form=form, pengaduan=pengaduan)

@gadmin.route("/detail-pengaduan/<int:ed_id>/detail", methods=['GET', 'POST'])
@login_required
def pengaduan_detail(ed_id):
    datapengaduan=Tpengaduan.query.get_or_404(ed_id)
    return render_template("t_admin/pengaduan-detail.html", datapengaduan=datapengaduan)

@gadmin.route("/pengaduann/<id>", methods=['GET', 'POST'])
@login_required
def hapus_pengaduan(id):
    h_pengaduan= Tpengaduan.query.get(id)
    db.session.delete(h_pengaduan)
    db.session.commit()
    flash('Data berhasil dihapus', 'warning')
    return redirect(url_for('gadmin.pengaduannn'))


#Bagian ADMIN
@gadmin.route("/login-admin", methods =['GET','POST'])
def loginadmin():
    if current_user.is_authenticated:
        return redirect(url_for('gadmin.dashboard'))
    form=login_admin()
    if form.validate_on_submit():
        cekemail=Tadmin.query.filter_by(email=form.email.data).first()
        if cekemail and bcrypt.check_password_hash(cekemail.password, form.password.data):
            login_user(cekemail)
            flash('Selamat Datang Kembali', 'warning')
            return redirect(url_for('gadmin.loginadmin'))
        else:
            flash('Login Gagal, Periksa Email dan Password Kembali', 'denger')
    return render_template("t_admin/login-admin.html", form=form)

@gadmin.route("/daftar-admin", methods =['GET','POST'])
def daftar_adm():
    form=df_admin()
    if form.validate_on_submit():
        file_foto=simpan_foto(form.foto.data)
        pass_hash=bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        add_admin=Tadmin(nama=form.nama.data, email=form.email.data, password=pass_hash,foto=file_foto)
        db.session.add(add_admin)
        db.session.commit()
        return redirect(url_for('gadmin.loginadmin'))
        flash(f'Akun- {form.nama.data} Berhasil Registrasi', 'warning')
    return render_template("t_admin/daftar-admin.html", form=form)


@gadmin.route("/pgrstuvwxyz", methods =['GET','POST'])
def dududu():
    form=daftar_admin()
    if form.validate_on_submit():
        file_foto=simpan_foto(form.foto.data)
        pass_hash=bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        add_admin=Tadmin(nama=form.nama.data, email=form.email.data, password=pass_hash,foto=file_foto)
        db.session.add(add_admin)
        db.session.commit()
        return redirect(url_for('gadmin.loginadmin'))
    return render_template("t_admin/adminn.html", form=form)

@gadmin.route("/edit-admin", methods=['GET', 'POST'])
@login_required
def editadmin():
    form=edit_admin()
    if form.validate_on_submit():
        if form.foto.data:
            file_foto=simpan_foto(form.foto.data)
            current_user.foto=file_foto
        pass_hash=bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        current_user.nama=form.nama.data
        current_user.email=form.email.data
        current_user.password=pass_hash
        db.session.commit()
        flash('Data Berhasil diubah','warning')
        return redirect(url_for('gadmin.dashboard'))
    elif request.method=="GET":
        form.nama.data=current_user.nama
        form.email.data=current_user.email
    return render_template("t_admin/edit_admin.html", form=form) 

@gadmin.route("/detail-admin", methods=['GET', 'POST'])
@login_required
def detail_admin():
    dataadminn=Tadmin.query.all()
    return render_template("t_admin/profil-admin.html", dataadminn=dataadminn)

@gadmin.route("/logout")
def logout_admin():
    logout_user()
    return redirect(url_for('gadmin.loginadmin'))

#Bagian Informasi
@gadmin.route("/informasi-admin", methods=['GET', 'POST'], defaults={"page": 1})
@gadmin.route("/informasi-admin/<int:page>", methods=['GET', 'POST'])
@login_required
def informasi(page):
    form=informasi_F()
    page = page
    pages = 10
    data=Tinformasi.query.all()
    informasi = Tinformasi.query.order_by(Tinformasi.id.desc()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form['tag']
        search ="%{}%".format(tag)
        informasi = Tinformasi.query.filter(Tinformasi.judul.like(search)).paginate(page, pages, error_out=False)
        return render_template("t_admin/informasi.html", informasi=informasi, form=form, tag=tag)
    if form.validate_on_submit():
        add= Tinformasi(judul=form.judul.data, informasi=form.informasi.data)
        db.session.add(add)
        db.session.commit()
        flash('Data berhasil ditambahkan','warning')
        return redirect(url_for('gadmin.informasi'))
    return render_template("t_admin/informasi.html", datainformasi=data, form=form, informasi=informasi)


@gadmin.route("/datainformasi-admin/<int:ed_id>/update", methods=['GET', 'POST'])
@login_required
def informasiedit(ed_id):
    dataadmin=Tadmin.query.all()
    datainformasi=Tinformasi.query.get_or_404(ed_id)  
    form=informasi_edit()
    if request.method=="GET":
        form.judul.data=datainformasi.judul
        form.informasi.data=datainformasi.informasi
    elif form.validate_on_submit():
        datainformasi.judul=form.judul.data
        datainformasi.informasi=form.informasi.data
        db.session.commit()
        flash('Data Berhasil Di ubah','warning')
        return redirect(url_for('gadmin.informasi'))
    return render_template("t_admin/informasi-edit.html", form=form,dataadmin=dataadmin)

@gadmin.route("/detail-informasiadmin/<int:ed_id>/detail", methods=['GET', 'POST'])
@login_required
def informasi_detail(ed_id):
    dataadmin=Tadmin.query.all()
    datainformasi=Tinformasi.query.get_or_404(ed_id)
    return render_template("t_admin/informasi-detail.html", datainformasi=datainformasi,dataadmin=dataadmin)

@gadmin.route("/informasii/<id>", methods=['GET', 'POST'])
@login_required
def hapus_informasi(id):
    h_informasi= Tinformasi.query.get(id)
    db.session.delete(h_informasi)
    db.session.commit()
    flash('Data berhasil dihapus', 'warning')
    return redirect(url_for('gadmin.informasi'))

#Bagian Informasi
@gadmin.route("/kegiatan-admin", methods=['GET', 'POST'], defaults={"page": 1})
@gadmin.route("/kegiatan-admin/<int:page>", methods=['GET', 'POST'])
@login_required
def kegiatan(page):
    form=kegiatan_F()
    page = page
    pages = 10
    data=Tdata_kegiatan.query.all()
    kegiatan= Tdata_kegiatan.query.order_by(Tdata_kegiatan.id.desc()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        kegiatan = Tdata_kegiatan.query.filter(Tdata_kegiatan.judul.like(search)).paginate(page, pages, error_out=False)
        return render_template("t_admin/kegiatan.html", kegiatan=kegiatan, form=form, tag=tag)
    if form.validate_on_submit():
        add=Tdata_kegiatan(tahun=form.tahun.data, judul=form.judul.data, program=form.program.data,bidang=form.bidang.data,status=form.status.data)
        db.session.add(add)
        db.session.commit()
        flash('Data berhasil ditambahkan','warning')
        return redirect(url_for('gadmin.kegiatan'))
    return render_template("t_admin/kegiatan.html", datakegiatan=data, form=form, kegiatan=kegiatan)

@gadmin.route("/datakegiatan-admin/<int:ed_id>/update", methods=['GET', 'POST'])
@login_required
def kegiatanedit(ed_id):
    dataadmin=Tadmin.query.all()
    datakegiatan=Tdata_kegiatan.query.get_or_404(ed_id)  
    form=kegiatan_edit()
    if request.method=="GET":
        form.tahun.data=datakegiatan.tahun
        form.judul.data=datakegiatan.judul
        form.program.data=datakegiatan.program
        form.bidang.data=datakegiatan.bidang
        form.status.data=datakegiatan.status
    elif form.validate_on_submit():
        datakegiatan.tahun=form.tahun.data
        datakegiatan.judul=form.judul.data
        datakegiatan.program=form.program.data
        datakegiatan.bidang=form.bidang.data
        datakegiatan.status=form.status.data
        db.session.commit()
        flash('Data Berhasil Di ubah','warning')
        return redirect(url_for('gadmin.kegiatan'))
    return render_template("t_admin/kegiatan-edit.html", form=form,dataadmin=dataadmin)

@gadmin.route("/detail-kegiatan/<int:ed_id>/detail", methods=['GET', 'POST'])
@login_required
def kegiatan_detail(ed_id):
    dataadmin=Tadmin.query.all()
    datakegiatan=Tdata_kegiatan.query.get_or_404(ed_id)
    return render_template("t_admin/kegiatan-detail.html", datakegiatan=datakegiatan,dataadmin=dataadmin)

@gadmin.route("/kegiatan/<id>", methods=['GET', 'POST'])
@login_required
def hapus_kegiatan(id):
    h_kegiatan= Tdata_kegiatan.query.get(id)
    db.session.delete(h_kegiatan)
    db.session.commit()
    flash('Data berhasil dihapus', 'warning')
    return redirect(url_for('gadmin.kegiatan'))
