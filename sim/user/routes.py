from re import S

from flask_wtf import form
from sim.admin.routes import dtumum_filter, struktur
from flask import Flask, render_template, redirect, url_for, Blueprint, flash, request
from sim import app,db,bcrypt
from sim.models import Tdata_kegiatan, Tdataumumfilter, Tprofil, Tdataumum, Tdatasekolah, Takresklh, Tkecamatan, Tpengaduan, Tadmin, Tberita, Tinformasi, Tstruktur, Tartikel
from sim.user.forms import pengaduan_F,editpengaduan_F
import os
import secrets
from sim import app
from PIL import Image

guser= Blueprint('guser',__name__)

@guser.route("/about")
def profill():
    dt_profil=Tprofil.query.all()
    return render_template("t_user2/profil.html", dt_profil=dt_profil)

@guser.route("/", methods=['GET', 'POST'], defaults={"page": 1})
@guser.route("//<int:page>", methods=['GET', 'POST'])
def home(page):
    page = page
    pages = 3
    dt_struktur=Tstruktur.query.all()
    datastruktur= Tstruktur.query.paginate(page=page, per_page=4)
    dt_program=Tdata_kegiatan.query.all()
    dataprogram= Tdata_kegiatan.query.order_by(Tdata_kegiatan.id.desc()).paginate(page, pages, error_out=False)
    dt_umum=Tdataumum.query.all()
    dt_informasi=Tinformasi.query.all()
    datainformasi= Tinformasi.query.order_by(Tinformasi.id.desc()).paginate(page, pages, error_out=False)
    dt_berita=Tberita.query.all()
    dt_artikel=Tartikel.query.all()
    dataartikel= Tartikel.query.order_by(Tartikel.id.desc()).paginate(page=page, per_page=2)
    databerita= Tberita.query.order_by(Tberita.id.desc()).paginate(page, pages, error_out=False)
    dtfilter=Tdataumumfilter.query.all()
    for filter in dtfilter:
        s = filter
    dtumum_now = Tdataumum.query.filter_by(tahun=str(s.tahun)).all()
    return render_template("t_user2/landing.html", dt_program=dt_program, dt_umum=dt_umum, dt_informasi=dt_informasi, dtumum_now=dtumum_now, dt_berita=dt_berita, databerita=databerita, dataprogram=dataprogram, datainformasi=datainformasi,dt_struktur=dt_struktur,datastruktur=datastruktur,dt_artikel=dt_artikel,dataartikel=dataartikel)

@guser.route("/base", methods=['GET', 'POST'])
def base():
    form=pengaduan_F()
    data=Tpengaduan.query.all()
    if form.validate_on_submit():
        add= Tpengaduan(email=form.email.data,kategori=form.kategori.data,detail_pengaduan=form.detail_pengaduan.data)
        flash('Pengaduan anda berhasil di input, tunggu 2x24 jam untuk membuat pengaduan kembali dengan email yang sama','secondary')
        db.session.add(add)
        db.session.commit()
        return redirect(url_for('guser.home'))
    return render_template("t_user2/base.html", datapengaduan=data, form=form)


@guser.route("/detail-kegiatan", methods=['GET', 'POST'], defaults={"page": 1})
@guser.route("/detail-kegiatan/<int:page>", methods=['GET', 'POST'])
def datakegiatan(page):
    page = page
    pages = 7
    data=Tdata_kegiatan.query.all()
    datakegiatan = Tdata_kegiatan.query.order_by(Tdata_kegiatan.id.desc()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search ="%{}%".format(tag)
        datakegiatan = Tdata_kegiatan.query.filter(Tdata_kegiatan.judul.like(search)).paginate(page, pages, error_out=False)
        return render_template("t_user2/program-kerja.html", datakegiatan=datakegiatan, tag=tag)
    return render_template("t_user2/program-kerja.html", datakegiatann=data, datakegiatan=datakegiatan)

@guser.route("/informasi", methods=['GET', 'POST'], defaults={"page": 1})
@guser.route("/informasi/<int:page>", methods=['GET', 'POST'])
def datainformasi(page):
    page = page
    pages = 5
    data=Tinformasi.query.all()
    datainformasi = Tinformasi.query.order_by(Tinformasi.id.desc()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search ="%{}%".format(tag)
        datainformasi = Tinformasi.query.filter(Tinformasi.judul.like(search)).paginate(page, pages, error_out=False)
        return render_template("t_user2/informasi.html", datainformasi=datainformasi, tag=tag)
    return render_template("t_user2/informasi.html", informasiii=data, datainformasi=datainformasi)


@guser.route("/detail-informasi/<int:ed_id>/detail", methods=['GET', 'POST'])
def informasi_detail(ed_id):
    datainformasi=Tinformasi.query.get_or_404(ed_id)
    return render_template("t_user2/informasi-detail.html", datainformasi=datainformasi)


@guser.route("/dashboard-user")
def dasboard():
    return render_template("t_user/index.html")

@guser.route("/struktur-orgnssi", methods=['GET', 'POST'], defaults={"page": 1})
@guser.route("/struktur-orgnssi/<int:page>", methods=['GET', 'POST'])
def datastruktur(page):
     page = page
     pages = 10
     dataa=Tstruktur.query.all()
     datastruktur = Tstruktur.query.paginate(page, pages, error_out=False)
     if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search ="%{}%".format(tag)
        datastruktur = Tstruktur.query.filter(Tstruktur.judul.like(search)).paginate(page, pages, error_out=False)
        return render_template("t_user2/strukturorganisasi.html", datastruktur=datastruktur, tag=tag)
     return render_template("t_user2/strukturorganisasi.html", struktur=dataa, datastruktur=datastruktur)

@guser.route("/datasekolahh", methods=['GET', 'POST'], defaults={"page": 1})
@guser.route("/datasekolahh/<int:page>", methods=['GET', 'POST'])
def datasekolah(page):
    page = page
    pages = 10
    data=Tdatasekolah.query.all()
    datasekolah = Tdatasekolah.query.order_by(Tdatasekolah.id.desc()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search ="%{}%".format(tag)
        datasekolah = Tdatasekolah.query.filter(Tdatasekolah.npsn.like(search)).paginate(page, pages, error_out=False)
        return render_template("t_user2/datasekolah.html", datasekolah=datasekolah, tag=tag)
    return render_template("t_user2/datasekolah.html", sekolah=data, datasekolah=datasekolah)

@guser.route("/dataumum", methods=['GET', 'POST'], defaults={"page": 1})
@guser.route("/dataumum/<int:page>", methods=['GET', 'POST'])
def dataumum(page):
    page = page
    pages = 10
    data=Tdataumum.query.all()
    dataumum = Tdataumum.query.order_by(Tdataumum.id.desc()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search ="%{}%".format(tag)
        dataumum = Tdataumum.query.filter(Tdataumum.tahun.like(search)).paginate(page, pages, error_out=False)
        return render_template("t_user2/dataumum.html", dataumum=dataumum, tag=tag)
    return render_template("t_user2/dataumum.html", dt_umum=data, dataumum=dataumum)

@guser.route("/detail-datasekolah/<int:ed_id>/detail", methods=['GET', 'POST'])
def datasekolah_detail(ed_id):
    datasekolah=Tdatasekolah.query.get_or_404(ed_id)
    return render_template("t_user2/detail-sekolah.html", datasekolah=datasekolah)


@guser.route("/beritaa", methods=['GET', 'POST'], defaults={"page": 1})
@guser.route("/beritaa/<int:page>", methods=['GET', 'POST'])
def berita(page):
    page = page
    pages = 3
    dt_berita=Tberita.query.all()
    berita = Tberita.query.order_by(Tberita.id.desc()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search ="%{}%".format(tag)
        berita = Tberita.query.filter(Tberita.judul.like(search)).paginate(page, pages, error_out=False)
        return render_template("t_user2/berita.html", berita=berita, tag=tag)
    return render_template("t_user2/berita.html", dt_berita=dt_berita, berita=berita)

@guser.route("/detail-berita/<int:ed_id>/detail", methods=['GET', 'POST'])
def berita_detail(ed_id):
    beritaa=Tberita.query.get_or_404(ed_id)
    return render_template("t_user2/beritaid.html", data=beritaa)


@guser.route("/artikel", methods=['GET', 'POST'], defaults={"page": 1})
@guser.route("/artikel/<int:page>", methods=['GET', 'POST'])
def dataartikell(page):
    page = page
    pages = 5
    data=Tartikel.query.all()
    dataartikel = Tartikel.query.order_by(Tartikel.id.desc()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search ="%{}%".format(tag)
        dataartikel = Tartikel.query.filter(Tartikel.judul.like(search)).paginate(page, pages, error_out=False)
        return render_template("t_user2/artikel.html", dataartikel=dataartikel, tag=tag)
    return render_template("t_user2/artikel.html", artikel=data, dataartikel=dataartikel)


@guser.route("/detail-artikel/<int:ed_id>/detail", methods=['GET', 'POST'])
def artikel_detail(ed_id):
    artikel=Tartikel.query.get_or_404(ed_id)
    return render_template("t_user2/artikelid.html", data=artikel)



