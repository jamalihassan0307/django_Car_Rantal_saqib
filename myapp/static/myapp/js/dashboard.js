// Get CSRF token from cookie
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Add headers to all fetch requests
const headers = {
  'X-CSRFToken': csrftoken,
  'Accept': 'application/json',
};

// Search functionality
document.getElementById('searchInput').addEventListener('input', function(e) {
  const searchTerm = e.target.value.toLowerCase();
  const statusFilter = document.getElementById('statusFilter').value;
  filterCars(searchTerm, statusFilter);
});

document.getElementById('statusFilter').addEventListener('change', function(e) {
  const searchTerm = document.getElementById('searchInput').value.toLowerCase();
  const statusFilter = e.target.value;
  filterCars(searchTerm, statusFilter);
});

function filterCars(searchTerm, statusFilter) {
  const cards = document.querySelectorAll('.car-card');
  cards.forEach(card => {
    const name = card.querySelector('h3').textContent.toLowerCase();
    const status = card.querySelector('.status').textContent.toLowerCase();
    const matchesSearch = name.includes(searchTerm);
    const matchesStatus = statusFilter === 'all' || status === statusFilter;
    card.style.display = matchesSearch && matchesStatus ? 'block' : 'none';
  });
}

// Modal functionality
const modals = document.querySelectorAll('.modal');
const closeButtons = document.querySelectorAll('.close');

closeButtons.forEach(btn => {
  btn.onclick = function() {
    this.closest('.modal').style.display = 'none';
  };
});

window.onclick = function(e) {
  if (e.target.classList.contains('modal')) {
    e.target.style.display = 'none';
  }
};

// Add Car functionality
if (document.getElementById('addCarBtn')) {
  document.getElementById('addCarBtn').onclick = function() {
    document.getElementById('addCarModal').style.display = 'block';
  };

  document.getElementById('addCarForm').onsubmit = async function(e) {
    e.preventDefault();
    const formData = new FormData(this);

    try {
      const response = await fetch('/cars/add/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
        },
        body: formData
      });

      const data = await response.json();
      if (data.success) {
        alert(data.message);
        window.location.reload();
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred while adding the car');
    }
  };
}

// Edit Car functionality
document.querySelectorAll('.edit-btn').forEach(btn => {
  btn.onclick = async function(e) {
    e.stopPropagation();
    const carId = this.dataset.carId;
    const card = this.closest('.car-card');
    const form = document.getElementById('editCarForm');
    
    // Fill the form with current values
    form.querySelector('#editCarId').value = carId;
    form.querySelector('#editCarName').value = card.querySelector('h3').textContent;
    form.querySelector('#editCarModel').value = card.querySelector('.car-info p').textContent.replace('Model: ', '');
    form.querySelector('#editCarStatus').value = card.querySelector('.status').textContent.toLowerCase();
    
    document.getElementById('editCarModal').style.display = 'block';
  };
});

document.getElementById('editCarForm').onsubmit = async function(e) {
  e.preventDefault();
  const carId = this.querySelector('#editCarId').value;
  const formData = new FormData(this);

  try {
    const response = await fetch(`/cars/edit/${carId}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
      },
      body: formData
    });

    const data = await response.json();
    if (data.success) {
      alert(data.message);
      window.location.reload();
    } else {
      alert(data.message);
    }
  } catch (error) {
    console.error('Error:', error);
    alert('An error occurred while updating the car');
  }
};

// Delete Car functionality
document.querySelectorAll('.delete-btn').forEach(btn => {
  btn.onclick = async function(e) {
    e.stopPropagation();
    if (confirm('Are you sure you want to delete this car?')) {
      const carId = this.dataset.carId;
      try {
        const response = await fetch(`/cars/delete/${carId}/`, {
          method: 'POST',
          headers: {
            ...headers,
            'Content-Type': 'application/json',
          },
        });

        const data = await response.json();
        if (data.success) {
          this.closest('.car-card').remove();
          alert(data.message);
        } else {
          alert(data.message);
        }
      } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while deleting the car');
      }
    }
  };
});

// Rent Car functionality
document.querySelectorAll('.rent-btn').forEach(btn => {
  btn.onclick = async function(e) {
    e.stopPropagation();
    if (confirm('Are you sure you want to rent this car?')) {
      const carId = this.dataset.carId;
      try {
        const response = await fetch(`/cars/rent/${carId}/`, {
          method: 'POST',
          headers: {
            ...headers,
            'Content-Type': 'application/json',
          },
        });

        const data = await response.json();
        if (data.success) {
          window.location.reload();
        } else {
          alert(data.message);
        }
      } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while renting the car');
      }
    }
  };
});

// Return Car functionality
document.querySelectorAll('.return-btn').forEach(btn => {
  btn.onclick = async function(e) {
    e.stopPropagation();
    if (confirm('Are you sure you want to return this car?')) {
      const carId = this.dataset.carId;
      try {
        const response = await fetch(`/cars/return/${carId}/`, {
          method: 'POST',
          headers: {
            ...headers,
            'Content-Type': 'application/json',
          },
        });

        const data = await response.json();
        if (data.success) {
          window.location.reload();
        } else {
          alert(data.message);
        }
      } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while returning the car');
      }
    }
  };
}); 