<template>
  <q-page>
    <div class="row justify-center">
      <div class="col-1"></div>
      <div class="col-2 gt-md"></div>
      <div class="col q-mt-md">
        <div class="text-h3 text-weight-light q-my-md">About</div>

        <h4 id="feedback">The Team</h4>

        <q-list class="justify-evenly">
          <q-item
            tag="a"
            href="https://www.linkedin.com/in/ivan-katkov-9556ab48/"
          >
            <!-- <q-item-section avatar>
              <q-avatar size="80px">
                <q-img src="avas/ava_IK.jpg" />
              </q-avatar>
            </q-item-section> -->
            <q-item-section>
              <q-item-label class="text-h5">Ivan Katkov</q-item-label>
              <q-item-label class="text-subtitle1"
                >New York University Abu Dhabi / Sternberg Astronomical
                Institute, Moscow State University</q-item-label
              >
              <q-item-label class="text-subtitle2">Researcher</q-item-label>
            </q-item-section>
          </q-item>

          <q-item
            tag="a"
            href="https://www.linkedin.com/in/damir-gasymov-b387361b8/"
          >
            <!-- <q-item-section avatar>
              <q-avatar size="80px">
                <q-img src="avas/ava_KG.jpg" />
              </q-avatar>
            </q-item-section> -->
            <q-item-section>
              <q-item-label class="text-h5">Damir Gasymov</q-item-label>
              <q-item-label class="text-subtitle1">
                Moscow State University</q-item-label
              >
              <q-item-label class="text-subtitle2">Student</q-item-label>
            </q-item-section>
          </q-item>

          <q-item
            tag="a"
            href="https://www.linkedin.com/in/joseph-gelfand-29324a10/"
          >
            <!-- <q-item-section avatar>
              <q-avatar size="80px">
                <q-img src="avas/ava_IK.jpg" />
              </q-avatar>
            </q-item-section> -->
            <q-item-section>
              <q-item-label class="text-h5">Joseph D. Gelfand</q-item-label>
              <q-item-label class="text-subtitle1"
                >New York University Abu Dhabi</q-item-label
              >
              <q-item-label class="text-subtitle2">Professor</q-item-label>
            </q-item-section>
          </q-item>

          <q-item tag="a" href="https://orcid.org/0000-0003-3599-3877">
            <!-- <q-item-section avatar>
              <q-avatar size="80px">
                <q-img src="avas/ava_VT.jpg" />
              </q-avatar>
            </q-item-section> -->
            <q-item-section>
              <q-item-label class="text-h5">Viktoria Toptun</q-item-label>
              <q-item-label class="text-subtitle1"
                >Moscow State University</q-item-label
              >
              <q-item-label class="text-subtitle2">Student</q-item-label>
            </q-item-section>
          </q-item>

          <q-item
            tag="a"
            href="https://www.linkedin.com/in/kirill-grishin-61560312b/"
          >
            <!-- <q-item-section avatar>
              <q-avatar size="80px">
                <q-img src="avas/ava_KG.jpg" />
              </q-avatar>
            </q-item-section> -->
            <q-item-section>
              <q-item-label class="text-h5">Kirill Grishin</q-item-label>
              <q-item-label class="text-subtitle1">
                Observatoire de Paris / SAI MSU</q-item-label
              >
              <q-item-label class="text-subtitle2">PhD Student</q-item-label>
            </q-item-section>
          </q-item>

          <q-item tag="a" href="https://orcid.org/0000-0002-8220-0756/">
            <!-- <q-item-section avatar>
              <q-avatar size="80px">
                <q-img src="avas/ava_KG.jpg" />
              </q-avatar>
            </q-item-section> -->
            <q-item-section>
              <q-item-label class="text-h5">Anton Afanasiev</q-item-label>
              <q-item-label class="text-subtitle1">
                Observatoire de Paris / SAI MSU</q-item-label
              >
              <q-item-label class="text-subtitle2">PhD Student</q-item-label>
            </q-item-section>
          </q-item>

          <q-item tag="a" href="https://www.linkedin.com/in/igorchilingarian">
            <!-- <q-item-section avatar>
              <q-avatar size="80px">
                <q-img src="avas/ava_IC.jpg" />
              </q-avatar>
            </q-item-section> -->
            <q-item-section>
              <q-item-label class="text-h5">Igor Chilingarian</q-item-label>
              <q-item-label class="text-subtitle1"
                >Harvard-Smithsonian Center for Astrophysics / SAI
                MSU</q-item-label
              >
              <q-item-label class="text-subtitle2">Researcher</q-item-label>
            </q-item-section>
          </q-item>

          <q-item tag="a" href="https://orcid.org/0000-0002-1091-5146">
            <!-- <q-item-section avatar>
              <q-avatar size="80px">
                <q-img src="avas/ava_VG.jpg" />
              </q-avatar>
            </q-item-section> -->
            <q-item-section>
              <q-item-label class="text-h5">Anastasia Kasparova</q-item-label>
              <q-item-label class="text-subtitle1"
                >Sternberg Astronomical Institute, Moscow State
                University</q-item-label
              >
              <q-item-label class="text-subtitle2">Researcher</q-item-label>
            </q-item-section>
          </q-item>

          <q-item tag="a" href="https://orcid.org/0000-0001-8427-0240">
            <!-- <q-item-section avatar>
              <q-avatar size="80px">
                <q-img src="avas/ava_ER.jpg" />
              </q-avatar>
            </q-item-section> -->
            <q-item-section>
              <q-item-label class="text-h5">Evgenii Rubtsov</q-item-label>
              <q-item-label class="text-subtitle1"
                >Moscow State University</q-item-label
              >
              <q-item-label class="text-subtitle2">PhD student</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>

        <h4 id="feedback">Feedback</h4>
        <p class="text-body1">
          The website is experimental and works in β mode, so some features may
          not work properly. If you believe you came across its malfunction, or
          want to request a new feature, please
          <a href="mailto:admin@voxastro.org">email</a> site authors.
        </p>

        <h4 id="ack">Acknowledgments</h4>
        <!-- <p>
          If the Reference Catalog of galaxy SEDs and this website are useful
          for your research, please include the link
          <a href="https://rcsed2.voxastro.org">https://rcsed2.voxastro.org</a>
          and cite these papers in any emerging publication:
        </p>
        <ul>
          <li>
            Chilingarian, I., Zolotukhin, I., Katkov, I., Melchior, A.-L. 2016:
            <a
              href="https://ui.adsabs.harvard.edu/abs/2017ApJS..228...14C/abstract"
              >RCSED — A Value-Added Reference Catalog of Spectral Energy
              Distributions of 800,299 Galaxies in 11 Ultraviolet, Optical, and
              Near-Infrared Bands: Morphologies, Colors, Ionized Gas and Stellar
              Populations Properties</a
            >, ApJS, v. 228, p. 25 (2017) &nbsp; [<a
              href="https://arxiv.org/pdf/1612.02047"
              >PDF</a
            >]
          </li>
          <li>
            Chilingarian, I., Zolotukhin, I. 2012:
            <a
              href="https://ui.adsabs.harvard.edu/abs/2012MNRAS.419.1727C/abstract"
              >A universal ultraviolet-optical colour-colour-magnitude relation
              of galaxies</a
            >, MNRAS, v. 419, p. 1727 &nbsp; [<a
              href="https://arxiv.org/pdf/1102.1159"
              >PDF</a
            >]
          </li>
        </ul> -->

        <p class="text-body1">
          This project has benefited from the support of Russian Science
          Foundation grant no. 21-72-00036.
        </p>

        <h4>Technologies</h4>

        <p class="text-body1">
          IFU Visualiser web-applcation inherits from first prototype of MaNGA
          Visualiser (<a href="https://manga.voxastro.org" target="_blank"
            >manga.voxastro.org</a
          >) and RCSEDv2 catalog (<a
            href="https://rcsed2.voxastro.org"
            target="_blank"
            >rcsed2.voxastro.org</a
          >).
        </p>

        <p class="text-body1">
          We would also like to acknowledge the usage of these technologies:
        </p>
        <q-list class="row justify-around q-my-lg">
          <q-item tag="a" href="https://quasar.dev/">
            <q-item-section avatar>
              <img
                src="~assets/logos/quasar.svg
              "
                style="height: 50px"
              />
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-h5">Quasar</q-item-label>
              <q-item-label class="text-subtitle1">
                Vue.js based framework
              </q-item-label>
            </q-item-section>
          </q-item>

          <q-item tag="a" href="https://www.djangoproject.com/">
            <q-item-section avatar>
              <img src="~assets/logos/django.png" style="height: 30px" />
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-h5">Django</q-item-label>
              <q-item-label class="text-subtitle1">
                Web framework
              </q-item-label>
            </q-item-section>
          </q-item>

          <q-item tag="a" href="https://www.django-rest-framework.org/">
            <q-item-section avatar>
              <img src="~assets/logos/drf.png" style="height: 50px" />
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-h5">Django REST</q-item-label>
              <q-item-label class="text-subtitle1">
                Toolkit for building Web APIs.
              </q-item-label>
            </q-item-section>
          </q-item>

          <q-item tag="a" href="https://www.postgresql.org/">
            <q-item-section avatar>
              <img src="~assets/logos/postgres.png" style="height: 50px" />
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-h5">PostgreSQL</q-item-label>
              <q-item-label class="text-subtitle1">
                Database management system
              </q-item-label>
            </q-item-section>
          </q-item>

          <q-item tag="a" href="https://aladin.u-strasbg.fr/AladinLite/doc/">
            <q-item-section avatar>
              <img src="~assets/logos/aladin.png" style="height: 60px" />
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-h5">Aladin lite</q-item-label>
              <q-item-label class="text-subtitle1">
                Lightweight JavaScript version of the Aladin tool
              </q-item-label>
            </q-item-section>
          </q-item>

          <!-- <q-item tag="a" href="http://soft.g-vo.org/dachs">
            <q-item-section avatar>
              <img src="~assets/logos/dachs.png" style="height: 50px" />
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-h5">GAVO DaCHS</q-item-label>
              <q-item-label class="text-subtitle1">
                VO data center software suite
              </q-item-label>
            </q-item-section>
          </q-item> -->

          <!-- <q-item tag="a" href="https://jira.atlassian.com/">
            <q-item-section avatar>
              <img src="~assets/logos/jira.png" style="height: 70px" />
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-h5">Jira Software</q-item-label>
              <q-item-label class="text-subtitle1">
                Task tracking system
              </q-item-label>
            </q-item-section>
          </q-item> -->
        </q-list>
      </div>
      <div class="col-1"></div>
      <div class="col-2 gt-md"></div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'AboutPage',
})
</script>
