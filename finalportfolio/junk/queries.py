import matplotlib.pyplot as mpl
import numpy as np

from sqlalchemy import select, func, alias, all_, except_
from models import session, User, Purchase, Share

def popdist():
    popdist_query = (
        select(Movie.mtitle, Movie.maudrating)
    )

    mresult = session.execute(popdist_query).all()
    mres_nums = [ret.maudrating for ret in mresult]
    mres_nums = np.array(mres_nums)
    mresult = [(ret.mtitle, ret.maudrating) for ret in mresult]
    session.rollback()

    bin_edges = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    mpl.hist(mres_nums, bins=bin_edges)
    mpl.title("Movies' Popular Score Distribution")
    mpl.xlabel("Popcornmeter Score (%)")
    mpl.ylabel("Frequency")
    mpl.show()