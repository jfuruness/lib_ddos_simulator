class User:
  """Bob"""
  
  def __init__(self, num: int, suspicion: float = 0, bucket: Bucket = None)
  	"""Stores user values"""
    
    self.num = num
    self.suspicion = suspicion
    self.bucket = bucket


class Attacker(User):
  """Mal"""
  
  def attack(self):
    pass

  
class Bucket:
  """Bucket has users (alice)"""
  
  def __init__(self, users: list = [], max_users=10000000):
    """Stores users"""
    
    self.users = users
    self._max_users = max_users
    self.contains_attacker = False
    
  def __len__(self):
    """Length of bucket"""
    
    return len(self.users)
    
  def add_user(self, user):
    """Adds a user, returns True if added else False"""
    
    if len(self.users) > self._max_users:
      return False
    else:
      self.users.append(user)
      if isinstance(user, Attacker):
        self.contains_attacker = True
      return True
    
  def update_sus(self):
  	"""Updates suspicion for all users in bucket"""
    
		if self.contains_attacker:
      # TODO: Custom iterator here
      for user in self.users:
        # TODO: figure out what val to add here
    		user.suspicion += 1 / len(self.users)
    

    
class Simulation:
  """Can run a sim"""

  def __init__(self, num_rounds, num_good_users, num_attackers, threshold, num_buckets):
    """Saves parameters for the simulation"""

    self.num_rounds = num_rounds
    self.manager = Manager(num_buckets)
    self.users = [User(x) for x in range(num_good_users)] + [Attacker(x) for x in range(num_attackers)]
    for user in self.users:
      self.manager.add_user(user)
    # Goal is to provide as much service as possible
    # Keep as many users as you can, get rid of as many attackers as you can (asap)
    for turn in num_rounds:
      self.manager.seive_shuffle()
      



class Sieve_Sim(Simulation):
  """Runs seive sim"""

  def __init__(self, num_rounds, num_good_users, num_attackers, threshold, num_buckets):
    
    # Initializes Parent class
    super(Sieve_Sim, self).__init__(num_rounds, num_good_users, num_attackers,
                                    threshold, num_buckets)
      
class Manager:
  """Controls all buckets (Eve)"""
  
  def __init__(self, num_buckets: int):
    self.buckets = [Bucket() for _ in num_buckets]
    # Doesn't matter because will just circle back to first bucket
    self._next_bucket = 0
    
  def add_user(self, user: User): 
    # WALRUS???
    self._next_bucket += 1
    if self._next_bucket >= len(self.buckets):
      self._next_bucket = 0
    if not self.buckets[self._next_bucket].add_user(user):
      for bucket in self.buckets:
        bucket.add_user(user)
        # If succeeds exit loop
        return
    # If you've reached this point, user does not fit into any bucket
    # So we need to decide whether to leave user out or buy a new bucket
    # if we buy a new bucket we must load balance
    # Impliment later
    1/0
    
  def sieve_shuffle(self):
    # NOTES FOR LATER:
    # If good bucket, never move except to add to another good bucket
    # If bad bucket, split (but not too low)
    # Shuffle bad buckets in such a way as to better determine attackers
    # Actually - split buckets until attacker no longer attacks
    #	this is because we can heuristically determine when an attacker won't attack anymore
    # This will make it so that you never split too low
    
    
    # Gain info
    # one way to gain info - split buckets until they are no longer attacked
    # This will ensure that you never split too low
    # This will also increase your odds of finding attacker by 2
    # For your split buckets, whatever buckets don't get attacked, merge back in
    # This will keep your cost low
    # This will determine if an attacker has a lower bound with respect to users when attacking
    
    
    # Out of the split buckets that have been attacked - move people between buckets
    # ideas - check suspsicion compared to that of the bucket
    # Change suspicion exponentially based on how many turns you are in the same bucket
    #		and haven't been attacked
    self._update_sus()
    buckets_under_attack = sum(1 for x in self.buckets if x.contains_attacker)
    if buckets_under_attack == len(buckets):
      for i in range(int(len(self.buckets) * .25)):
        self.buckets.append(Bucket())
    
    
  def _update_sus(self):
		"""Updates suspicion level of all users"""
    
    for bucket in buckets:
			bucket.update_sus()
    
      


if __name__ == "__main__":
	Sieve_Sim(num_rounds=100, num_good_users=100, num_attackers=10,
            threshold=500, num_buckets=5).run_sieve_sim()
