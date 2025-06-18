using Crud.DAL.Interfaces;
using Crud.Model;
using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;

namespace CrudAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class UserController : ControllerBase
    {
        private readonly IUserDAL _userDAL;

        public UserController(IUserDAL userDAL)
        {
            _userDAL = userDAL;
        }

        [HttpGet]
        public async Task<IActionResult> GetAll()
        {
            return Ok(await _userDAL.GetAllAsync());
        }

        [HttpGet]
        [Route("{id}")]
        public async Task<IActionResult> GetAll([FromRoute] long id)
        {
            return Ok(await _userDAL.GetByIdAsync(id));
        }

        [HttpPost]
        public async Task<IActionResult> Insert([FromBody] User user)
        {
            await _userDAL.InsertAsync(user);

            return Ok();
        }

        [HttpPut]
        public async Task<IActionResult> Update([FromBody] User user)
        {
            await _userDAL.UpdateAsync(user);

            return Ok();
        }

        [HttpDelete]
        [Route("{id}")]
        public async Task<IActionResult> Delete([FromRoute] long id)
        {
            await _userDAL.DeleteAsync(await _userDAL.GetByIdAsync(id));

            return Ok();
        }
    }
}
