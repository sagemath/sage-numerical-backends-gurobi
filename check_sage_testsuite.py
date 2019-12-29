# Check portions of the sage test suite -- call this after patch_into_sage_module.py
import os
import sage.env
os.chdir(os.path.join(sage.env.SAGE_LIB, 'sage'))
os.system("sage-runtests -p "
          "coding "
          "combinat/designs combinat/integer_vector.py combinat/posets/ "
          "game_theory/ "
          "geometry/polyhedron/base.py geometry/cone.py "
          "graphs/ "
          "homology/simplicial_complex.py "
          "knots/ "
          "matroids/ "
          "numerical/*.py* "
          "sat/ ")
